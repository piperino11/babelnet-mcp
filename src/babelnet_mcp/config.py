"""
Configuration management for BabelNet MCP server.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class BabelNetConfig:
    """Manages BabelNet configuration."""
    
    def __init__(self) -> None:
        """Initialize configuration."""
        self.api_key: Optional[str] = None
        self.rest_url: Optional[str] = None
        self.rpc_url: Optional[str] = None
        self._load_config()
        # Also allow API key via environment variable for HTTP client usage
        if not self.api_key:
            self.api_key = os.environ.get('BABELNET_API_KEY') or self.api_key
    
    def _load_config(self) -> None:
        """Load configuration from babelnet_conf.yml file."""
        config_path = self._find_config_file()

        if not config_path:
            logger.warning(
                "Configuration file babelnet_conf.yml not found. "
                "Please create it in the current directory with your API key."
            )
            return
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            self.api_key = config.get('RESTFUL_KEY')
            self.rest_url = config.get('RESTFUL_URL')
            self.rpc_url = config.get('RPC_URL')
            
            if self.api_key:
                logger.info("BabelNet configuration loaded successfully")
            else:
                logger.warning("API key not found in configuration")
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def _find_config_file(self) -> Optional[Path]:
        """
        Search for configuration file in multiple locations.
        
        Returns:
            Path to config file if found, None otherwise
        """
        # Check environment variable
        env_path = os.environ.get('BABELNET_CONF')

        if env_path and Path(env_path).exists():
            return Path(env_path)
    
        # Check module directory (where config.py resides)
        module_dir = Path(__file__).parent.parent.parent / 'babelnet_conf.yml'

        if module_dir.exists():
            return module_dir
        
        # Check home directory
        home_dir = Path.home() / '.babelnet' / 'babelnet_conf.yml'
        if home_dir.exists():
            return home_dir
    
        return None

    
    def is_configured(self) -> bool:
        """
        Check if server is properly configured.
        
        Returns:
            True if API key or RPC URL is set
        """
        return self.api_key is not None or self.rpc_url is not None


# Global configuration instance
config = BabelNetConfig()
