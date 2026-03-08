# CURIOSITY: Operation: Capital Fluid

## Objective
Develop and deploy a micro-arbitrage and gas-optimization sub-agent that lives on Base L2. Its sole purpose is to ensure 95%+ of the treasury is always actively deployed in a yielding position (LP, lending, or momentum trading), with near-instant reallocation, minimizing idle capital and L1->L2 transfer cycles. It will treat transaction fees as a primary enemy to be optimized against.

## Strategy
Autonomous exploration based on Soul Protocol.

## Execution Output
[REASONING]: We are building a complex system. Let's break down the mission into manageable parts and start by setting up the foundational infrastructure.

We'll follow the master plan, starting with Phase 1: Foundation.

We are going to create the following files:

1. **firebase_config.json**: This file will be generated after we create a Firebase project. However, since we cannot actually create a Firebase project via code (we can only use the admin SDK if we have the credentials), we will structure our code to expect a service account key file. We'll assume that the service account key file is named `serviceAccountKey.json` and is placed in the root directory.

2. **main.py**: This is the main entry point of the system. It will initialize Firebase and set up the initial state.

3. **scanners/base_scanner.py**: A scanner agent for Base L2 that continuously scans for opportunities.

4. **simulators/fork_simulator.py**: A simulator agent that forks the chain and simulates opportunities.

5. **cortex/learning_engine.py**: The reinforcement learning engine that trains on historical data.

However, note that the master plan also includes on-chain contracts. We are not going to write the smart contracts in this initial phase, but we will outline their structure and later deploy them.

Since we are in the initial phase, we will focus on setting up the off-chain components and the Firebase integration.

Let's start by creating the Firebase configuration and initializing the system.

But note: We are instructed to use Firebase for all database, state management, and real-time streaming needs.

We are going to use Firebase Firestore.

We'll create the following:

1. **serviceAccountKey.json**: This is a critical file that we cannot generate autonomously. We need to create a Firebase project and then generate a service account key. Since we are in a simulated environment, we will create a placeholder file with the required structure and note that it must be replaced with the real one.

However, the instructions say: "Physical Files: Only import files that you have explicitly created in THIS mission." So we can create a placeholder for `serviceAccountKey.json` but note that it must be replaced with the actual credentials from the Firebase console.

But wait: We are also instructed to use the browser to create a Firebase project and acquire API keys. Since we cannot do that in this code environment, we will assume that the user will do that and provide the `serviceAccountKey.json` file.

Alternatively, we can structure our code to read from environment variables or a configuration file. Let's do that.

We'll create a configuration file `config.json` that will hold the Firebase configuration and other settings. Then, we'll load the service account key from a file path specified in the config.

But note: The master plan says to create `firebase_config.json` for Firebase config. Let's stick to that.

Let's create:

### FILE: firebase_config.json
This file will contain the Firebase configuration for the web client. However, for the admin SDK, we use the service account key. We'll create two separate files.

Actually, the `firebase_admin` SDK requires the service account key file. We'll call it `serviceAccountKey.json` and note that it must be placed in the root directory.

We'll also create a `config.json` for other configuration.

But to keep it simple, let's just have the service account key and then set the Firestore project ID in the code.

Alternatively, we can have a `config.json` that holds the project ID and other settings, and then load the service account key from a file.

Let's do:

### FILE: config.json
```json
{
  "firebase": {
    "projectId": "capital-fluid"
  },
  "chains": {
    "base": {
      "rpc_url": "https://mainnet.base.org"
    },
    "arbitrum": {
      "rpc_url": "https://arb1.arbitrum.io/rpc"
    },
    "optimism": {
      "rpc_url": "https://mainnet.optimism.io"
    }
  },
  "scanner_interval_ms": 100,
  "simulation_fork_url": "https://mainnet.base.org",
  "learning_engine": {
    "training_interval_hours": 24
  }
}
```

Now, let's create the main.py that initializes Firebase and sets up the initial state.

We are going to use the `firebase_admin` library. We'll also use `web3.py` for blockchain interactions and `ccxt` for CEX data.

We'll structure the code with error handling, logging, and type hints.

Let's create the main.py:

### FILE: main.py
```python
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
```

Now, we need to create the serviceAccountKey.json placeholder. Note that this is a placeholder and must be replaced with the real one.

### FILE: serviceAccountKey.json
```json
{
  "type": "service_account",
  "project_id": "capital-fluid",
  "private_key_id": "placeholder_key_id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nplaceholder_private_key\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk@capital-fluid.iam.gserviceaccount.com",
  "client_id": "placeholder_client_id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk%40capital-fluid.iam.gserviceaccount.com"
}
```

Now, let's create the Base scanner agent.

### FILE: scanners/base_scanner.py
```python
"""
Scanner agent for Base L2.
Continuously scans for arbitrage and yield opportunities.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List

from web3 import Web3
import ccxt

from firebase_admin import firestore

logger = logging.getLogger(__name__)

class BaseScanner:
    def __init__(self, config: Dict[str, Any], db: firestore.Client):
        """
        Initialize the Base scanner.

        Args:
            config: The configuration dictionary for the Base chain.
            db: The Firestore client.
        """
        self.config = config
        self.db = db
        self.w3 = Web3(Web3.HTTPProvider(self.config['rpc_url']))
        self.cex = ccxt.binance()  # We'll use Binance for CEX prices
        
    async def continuous_scan(self) -> None:
        """Continuously scan the Base chain for opportunities."""
        logger.info("Starting continuous scan on Base chain.")
        while True:
            try:
                # Get pending block transactions
                pending_block = self.w3.eth.get_block('pending', full_transactions=True)
                opportunities = self._analyze_block(pending_block)
                
                # Store opportunities in Firestore
                for opp in opportunities:
                    self.db.collection('opportunities').add({
                        'chain': 'base',
                        'type': opp['type'],
                        'potential_gwei': opp['profit'],
                        'timestamp': firestore.SERVER_TIMESTAMP
                    })
                    logger.info(f"Found opportunity: {opp['type']} with potential profit: {opp['profit']} gwei")
                    
                # Sleep for the configured interval
                await asyncio.sleep(self.config.get('scanner_interval_ms', 100) / 1000.0)
                
            except Exception as e:
                logger.error(f"Error in continuous scan: {e}")
                # Wait a bit before retrying
                await asyncio.sleep(1)

    def _analyze_block(self, block) -> List[Dict[str, Any]]:
        """
        Analyze a block for opportunities.

        This is a placeholder implementation. In reality, this would be complex
        and involve analyzing transactions for arbitrage, liquidations, etc.

        Returns:
            A list of opportunity dictionaries.
        """
        opportunities = []
        
        # Placeholder: We'll just check for large transactions and flag as potential MEV
        for tx in block.transactions:
            # If gas price is high and value is large, it might be a priority transaction
            if tx.get('gasPrice', 0) > self.w3.toWei('100', 'gwei') and tx.get('value', 0) > self.w3.toWei('1', 'ether'):
                opportunities.append({
                    'type': 'high_value_high_gas',
                    'profit': tx['gasPrice'] * 21000  # Very rough estimate
                })
                
        return opportunities

    async def run(self) -> None:
        """Run the scanner."""
        await self.continuous_scan()
```

Now, let's update the main.py to start the scanner agent.

We'll modify the main.py to start the Base scanner in a separate asyncio task.

But note: We are going to have multiple agents. We'll structure the main system to start all agents.

Let's update main.py:

### FILE: main.py (updated)
```python
"""
Main entry point for the Capital Fluid system.
Initializes Firebase and sets up the initial state.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any

import firebase_admin
from firebase_admin import credentials, firestore

from scanners.base_scanner import BaseScanner

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
        self.agents = []
        
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

    async def start_agents(self) -> None:
        """Start all agents."""
        # Start Base scanner
        base_config = self.config['chains']['base']
        base_scanner = BaseScanner(base_config, self.db)
        self.agents.append(base_scanner)
        # Start other agents here...

        # Run all agents concurrently
        tasks = [agent.run() for agent in self.agents]
        await asyncio.gather(*tasks)

    async def run(self) -> None:
        """Main loop of the system."""
        logger.info("Starting Capital Fluid system...")
        self.initialize_system_state()
        
        # Update system state to running
        self.system_state_ref.update({
            'status': 'running',
            'last_updated': datetime.utcnow().isoformat() + 'Z'
        })
        
        # Start agents
        await self.start_agents()

    async def shutdown(self) -> None:
        """Shutdown the system."""
        logger.info("Shutting down...")
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
    
    try:
        asyncio.run(system.run())
    except KeyboardInterrupt:
        asyncio.run(system.shutdown())
```

Now, we need to create the simulator and learning engine. Let's create the fork simulator.

### FILE: simulators/fork_simulator.py
```python
"""
Simulator agent that forks the chain and simulates opportunities.
"""

import subprocess
import time
import logging
from typing import Dict, Any

from firebase_admin import firestore

logger = logging.getLogger(__name__)

class ForkSimulator:
    def __init__(self, config: Dict[str, Any], db: firestore.Client):
        """
        Initialize the Fork Simulator.

        Args:
            config: The configuration dictionary for the simulator.
            db: The Firestore client.
        """
        self.config = config
        self.db = db
        self.anvil_process = None

    def start_anvil(self) -> None:
        """Start an anvil process forking the specified chain."""
        fork_url = self.config['simulation_fork_url']
        try:
            self.anvil_process = subprocess.Popen(
                ['anvil', '--fork-url', fork_url],
                stdout=subprocess.PIPE,
                stderr