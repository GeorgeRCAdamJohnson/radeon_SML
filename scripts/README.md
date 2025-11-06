# Scripts Directory

This directory contains utility scripts organized by purpose for the Radeon SML AI project.

## 📁 Directory Structure

### 🚀 [deployment/](deployment/)
Scripts for deploying the application to various environments.

**Batch Scripts (Windows):**
- `deploy_gcp.bat` - Google Cloud Platform deployment
- `deploy_gcp_secure.bat` - Secure GCP deployment with enhanced security
- `deploy_local.bat` - Local development deployment
- `docker_deploy.bat` - Docker container deployment
- `docker_stop.bat` - Stop Docker containers
- `nuclear_deploy.bat` - Complete reset and redeploy
- `restart_docker_deploy.bat` - Restart Docker deployment
- `setup_gcp.bat` - Initial GCP setup
- `start_server.bat` - Start local development server
- `check_status.bat` - Check deployment status

**Shell Scripts (Unix/Linux):**
- `deploy.sh` - Universal deployment script

### 🧹 [maintenance/](maintenance/)
Scripts for maintaining and updating the knowledge base and system.

**Python Scripts:**
- `clean_knowledge_base.py` - Clean and optimize knowledge base
- `validate_knowledge.py` - Validate knowledge base integrity
- `run_crawler.py` - Update knowledge base with new content

**Batch Scripts:**
- `run_ethics_crawler.bat` - Run ethics-specific content crawler

### 🧪 [testing/](testing/)
Testing and validation scripts (if any test scripts are moved here).

## 🚀 Deployment Scripts

### Quick Deploy Commands
```bash
# Windows (PowerShell)
.\scripts\deployment\deploy_gcp.bat

# Local development
.\scripts\deployment\start_server.bat

# Docker deployment
.\scripts\deployment\docker_deploy.bat

# Unix/Linux
./scripts/deployment/deploy.sh
```

### Deployment Script Features
- **Environment Detection**: Automatically detect and configure environments
- **Error Handling**: Comprehensive error checking and rollback
- **Security**: Secure credential handling and validation
- **Logging**: Detailed deployment logs for debugging
- **Validation**: Post-deployment health checks

## 🧹 Maintenance Scripts

### Knowledge Base Maintenance
```bash
# Clean and optimize
python scripts/maintenance/clean_knowledge_base.py

# Validate integrity
python scripts/maintenance/validate_knowledge.py

# Update content
python scripts/maintenance/run_crawler.py
```

### Maintenance Features
- **Data Validation**: Check for corrupted or invalid data
- **Performance Optimization**: Optimize database queries and indexes
- **Content Updates**: Automated content refresh from sources
- **Backup Management**: Create and manage data backups
- **Health Monitoring**: System health checks and reporting

## 🔧 Script Configuration

### Environment Variables
```bash
# Deployment Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
DEPLOYMENT_ENV=production|staging|development

# Maintenance Configuration  
KNOWLEDGE_BASE_PATH=./data/
BACKUP_PATH=./backups/
API_DELAY=2.0

# Security Configuration
SECURE_MODE=true
VALIDATE_SSL=true
```

### Configuration Files
Scripts use configuration from:
- `config/` directory files
- Environment variables
- Command line arguments
- Default fallback values

## 📝 Usage Guidelines

### Before Running Scripts
1. **Check Prerequisites**: Ensure required tools are installed
2. **Set Environment**: Configure environment variables
3. **Test Access**: Verify permissions and connectivity
4. **Backup Data**: Create backups before major operations

### Common Parameters
Most scripts support these common parameters:
- `--help` - Show usage information
- `--verbose` - Enable detailed output
- `--dry-run` - Preview actions without executing
- `--config` - Specify configuration file
- `--env` - Set target environment

### Error Handling
- All scripts include comprehensive error handling
- Logs are written to `logs/` directory
- Failed operations include rollback procedures
- Exit codes indicate success (0) or failure (non-zero)

## 🛡️ Security Considerations

### Credential Management
- Never hardcode credentials in scripts
- Use environment variables or secure vaults
- Rotate credentials regularly
- Validate permissions before execution

### Access Control
- Scripts require appropriate permissions
- Use principle of least privilege
- Log all script executions
- Monitor for unauthorized usage

## 🔍 Debugging Scripts

### Common Issues
1. **Permission Errors**: Check file/directory permissions
2. **Network Failures**: Verify connectivity and DNS
3. **Configuration Issues**: Validate environment variables
4. **Dependency Problems**: Ensure required tools are installed

### Debug Mode
```bash
# Enable debug output
DEBUG=true python scripts/maintenance/validate_knowledge.py

# Verbose logging
python scripts/maintenance/run_crawler.py --verbose

# Dry run mode
python scripts/maintenance/clean_knowledge_base.py --dry-run
```

## 📈 Performance Considerations

### Optimization Tips
- Run maintenance scripts during low-traffic periods
- Use parallel processing where appropriate
- Monitor resource usage during execution
- Implement rate limiting for external API calls

### Resource Usage
- **Memory**: Scripts are optimized for low memory usage
- **CPU**: Batch processing minimizes CPU spikes
- **Network**: Respectful API calling with delays
- **Storage**: Efficient disk space management

## 🚀 Adding New Scripts

### Script Template
```bash
#!/usr/bin/env python3
"""
Script Name: new_script.py
Purpose: Brief description of what this script does
Author: Your Name
Date: YYYY-MM-DD
"""

import argparse
import logging
import sys
from pathlib import Path

def setup_logging(verbose=False):
    """Configure logging for the script."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    """Main script function."""
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions only')
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    logging.info("Script starting...")
    
    try:
        # Script logic here
        pass
    except Exception as e:
        logging.error(f"Script failed: {e}")
        sys.exit(1)
    
    logging.info("Script completed successfully")

if __name__ == "__main__":
    main()
```

### Documentation Requirements
- Clear script purpose and usage
- Parameter documentation
- Example usage commands
- Error handling description
- Performance considerations

---

For questions about scripts, see the main project documentation or create an issue.