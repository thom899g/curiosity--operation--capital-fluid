"""
Main entry point for the Capital Fluid system.
Initializes Firebase and sets up the initial state.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any

import firebase_admin
from firebase_admin import credentials, firestore

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CapitalFluidSystem:
    def __init__(self, config_path: str = 'config.json'):
        """Initialize the Capital Fluid system with the given configuration."""
        self.config = self._load_config(config_path)
        self.db = self._init_firebase()
        self.system_state_ref = self.db.collection('system_state').document('v1')
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from a JSON file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file {config_path} not found.")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {config_path}: {e}")
            raise

    def _init_firebase(self) -> firestore.Client:
        """Initialize Firebase Admin SDK and return a Firestore client."""
        try:
            # Load the service account key
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred, {
                'projectId': self.config['firebase']['projectId']
            })
            logger.info("Firebase Admin SDK initialized successfully.")
            return firestore.client()
        except FileNotFoundError:
            logger.error("serviceAccountKey.json not found. Please download it from the Firebase console.")
            raise
        except ValueError as e:
            logger.error(f"Error initializing Firebase: {e}")
            raise

    def initialize_system_state(self) -> None:
        """Set the initial system state in Firestore."""
        initial_state = {
            'status': 'initializing',
            'treasury_eth': 0,
            'active_chains': [],
            'timestamp': firestore.SERVER_TIMESTAMP,
            'last_updated': datetime.utcnow().isoformat() + 'Z'
        }
        try:
            self.system_state_ref.set(initial_state)
            logger.info("Initial system state set in Firestore.")
        except Exception as e:
            logger.error(f"Error setting initial system state: {e}")
            raise

    def run(self) -> None:
        """Main loop of the system."""
        logger.info("Starting Capital Fluid system...")
        self.initialize_system_state()
        # TODO: Start scanner agents, learning engine, etc.
        logger.info("System is running. Press Ctrl+C to stop.")
        # Keep the program running
        try:
            while True:
                # For now, just sleep
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            # Update system state to shutting down
            self.system_state_ref.update({
                'status': 'shutting_down',
                'last_updated': datetime.utcnow().isoformat() + 'Z'
            })
            logger.info("System state updated to shutting down.")

if __name__ == "__main__":
    # Check if the service account key exists
    import os
    if not os.path.exists('serviceAccountKey.json'):
        logger.error("serviceAccountKey.json not found. Please place it in the root directory.")
        sys.exit(1)
        
    system = CapitalFluidSystem()
    system.run()