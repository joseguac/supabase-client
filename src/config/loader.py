"""
Configuration loader
Handles loading and validation of configuration settings from various sources.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

from .constants import (
    DATA_FILES, DEFAULTS, MESSAGES,
    get_data_file_paths, get_required_env_vars
)


class ConfigLoader:
    """Configuration loader that handles environment-specific settings."""
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize the configuration loader.
        
        Args:
            base_path: Base directory path for the application
        """
        self.base_path = base_path or Path(__file__).parent.parent.parent
        self._config_cache: Dict[str, Any] = {}
    
    def load_environment_variables(self, env_file_path: Optional[Path] = None) -> Dict[str, str]:
        """
        Load environment variables from .env file and system environment.
        
        Args:
            env_file_path: Optional path to .env file
            
        Returns:
            Dictionary of loaded environment variables
        """
        if 'env_vars' in self._config_cache:
            return self._config_cache['env_vars']
        
        # Load .env file if it exists
        env_file = env_file_path or (self.base_path / DEFAULTS['ENV_FILE'])
        if env_file.exists():
            load_dotenv(env_file)
        
        # Load required environment variables (hardcoded as they are standard)
        env_vars = {}
        required_vars = ['SUPABASE_URL', 'API_Key']
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                env_vars[var] = value
            else:
                raise ValueError(f"Required environment variable {var} not found")
        
        self._config_cache['env_vars'] = env_vars
        return env_vars
    
    def get_file_paths(self) -> Dict[str, Path]:
        """
        Get all configured file paths.
        
        Returns:
            Dictionary mapping file types to their paths
        """
        if 'file_paths' in self._config_cache:
            return self._config_cache['file_paths']
        
        file_paths = get_data_file_paths(self.base_path)
        self._config_cache['file_paths'] = file_paths
        return file_paths
    
    def validate_configuration(self) -> bool:
        """
        Validate that all required configuration is available.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Check environment variables
            self.load_environment_variables()
            
            # Check file paths
            file_paths = self.get_file_paths()
            
            # Validate that data files exist
            for file_type, file_path in file_paths.items():
                if file_type.endswith('_file') and not file_path.exists():
                    if file_type == 'env_file':
                        continue  # .env file is optional
                    raise FileNotFoundError(f"Required file not found: {file_path}")
            
            return True
            
        except Exception as e:
            print(f"{MESSAGES['ERROR_PREFIX']} Configuration validation failed: {e}")
            return False
    
    def get_supabase_config(self) -> Dict[str, str]:
        """
        Get Supabase configuration from environment variables.
        
        Returns:
            Dictionary with Supabase URL and API key
        """
        env_vars = self.load_environment_variables()
        return {
            'url': env_vars['SUPABASE_URL'],
            'key': env_vars['API_Key']
        }
    
    def get_data_config(self) -> Dict[str, Any]:
        """
        Get data configuration including file paths and settings.
        
        Returns:
            Dictionary with data configuration
        """
        file_paths = self.get_file_paths()
        return {
            'file_paths': file_paths,
            'verify_data': DEFAULTS['VERIFY_DATA'],
            'clear_existing': DEFAULTS['CLEAR_EXISTING'],
            'encoding': DEFAULTS['ENCODING']
        }
    
    def clear_cache(self) -> None:
        """Clear the configuration cache to force reload."""
        self._config_cache.clear()


def get_config_loader(base_path: Optional[Path] = None) -> ConfigLoader:
    """
    Get a configured ConfigLoader instance.
    
    Args:
        base_path: Optional base path for the application
        
    Returns:
        Configured ConfigLoader instance
    """
    return ConfigLoader(base_path)
