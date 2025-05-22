import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Email Configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "hetprajapati122@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "mxopsocrsmgufotm")
    
    # Scraping Configuration
    DELAY_BETWEEN_REQUESTS = 2  # seconds
    MAX_RETRIES = 3
    BATCH_SIZE = 5  # emails per batch
    DELAY_BETWEEN_BATCHES = 30  # seconds
    
    # ICP Configuration
    TARGET_INDUSTRIES = [
        "Technology", "Software", "SaaS", "E-commerce",
        "Digital Marketing", "Consulting"
    ]
    TARGET_LOCATIONS = ["United States", "Canada", "United Kingdom"]
    COMPANY_SIZE_RANGE = "10-500 employees"
    
    # File Paths
    LEADS_FILE = "data/leads.xlsx"
    TEMPLATE_FILE = "templates/email_template.html"
    LOG_FILE = "logs/campaign_log.csv"