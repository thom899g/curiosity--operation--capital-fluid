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