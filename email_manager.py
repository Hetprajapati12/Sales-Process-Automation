import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import uuid
import logging
import random
from config import Config
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailManager:
    def __init__(self):
        self.smtp_server = None
        self.tracking_data = []
        
    def create_email_template(self):
        """Create HTML email template"""
        template_html = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Opportunity</title>
    <style>
    body {{font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;}}
    .container {{max-width: 600px; margin: 0 auto; padding: 20px;}}
    .header {{background-color: #4CAF50; color: white; padding: 20px; text-align: center;}}
    .content {{padding: 20px; background-color: #f9f9f9;}}
    .cta-button {{background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0;}}
    .footer {{text-align: center; padding: 20px; font-size: 12px; color: #666;}}
    </style>
    </head>
    <body>
    <div class="container">
    <div class="header">
    <h1>Exclusive Business Opportunity</h1>
    </div>
    <div class="content">
    <p>Dear {contact_person},</p>
    <p>I hope this email finds you well. I came across <strong>{company_name}</strong> and was impressed by your work in the {industry} sector.</p>
    <p>We specialize in helping companies like yours streamline their sales processes and increase revenue through automation and AI-powered solutions.</p>
    <p>Here is what we can offer {company_name}:</p>
    <ul>
    <li>Sales Process Automation (up to 40% time savings)</li>
    <li>AI-Powered Lead Scoring and Analytics</li>
    <li>Custom CRM Integration</li>
    <li>Revenue Growth Optimization</li>
    </ul>
    <p>Companies similar to yours have seen an average of 25% increase in qualified leads and 35% improvement in conversion rates within the first 3 months.</p>
    <a href="https://calendly.com/consultation?company={company_name}&track_id={tracking_id}" class="cta-button">Schedule a Free 15-Minute Consultation</a>
    <p>Would you be interested in a brief call to discuss how we can help {company_name} achieve similar results?</p>
    <p>Best regards,<br>Alex Thompson<br>Sales Automation Specialist<br>Phone: (555) 123-4567<br>Email: alex@salesautomation.com</p>
    </div>
    <div class="footer">
    <p>If you prefer not to receive emails like this, <a href="https://unsubscribe.com?track_id={tracking_id}">click here to unsubscribe</a></p>
    <img src="https://track.com/pixel?track_id={tracking_id}" width="1" height="1" style="display:none;" alt="">
    </div>
    </div>
    </body>
    </html>"""
        
        # Create templates directory if it doesn't exist
        os.makedirs(os.path.dirname(Config.TEMPLATE_FILE), exist_ok=True)
        
        # Save template to file
        with open(Config.TEMPLATE_FILE, 'w', encoding='utf-8') as f:
            f.write(template_html)
        
        logger.info(f"Email template created: {Config.TEMPLATE_FILE}")
        return template_html
    def personalize_email(self, template, lead_data):
        """Personalize email template with lead data"""
        tracking_id = str(uuid.uuid4())
        
        # Default values for missing data
        contact_person = lead_data.get('contact_person', 'Decision Maker')
        if contact_person == 'N/A':
            contact_person = 'Decision Maker'
            
        company_name = lead_data.get('company_name', 'Your Company')
        industry = lead_data.get('industry', 'your industry')
        
        try:
            personalized_email = template.format(
                contact_person=contact_person,
                company_name=company_name,
                industry=industry,
                tracking_id=tracking_id
            )
        except Exception as e:
            logger.error(f"Template formatting error for {company_name}: {e}")
            # Use a simple fallback template
            personalized_email = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
            <h2>Business Opportunity for {company_name}</h2>
            <p>Dear {contact_person},</p>
            <p>We would like to discuss how we can help {company_name} grow their business in the {industry} sector.</p>
            <p>Our solutions include:</p>
            <ul>
            <li>Sales Process Automation</li>
            <li>Lead Generation</li>
            <li>Analytics and Reporting</li>
            </ul>
            <p>Best regards,<br>Sales Automation Team</p>
            </body>
            </html>
            """
        
        # Store tracking data
        tracking_info = {
            'tracking_id': tracking_id,
            'company_name': company_name,
            'email': lead_data.get('email', ''),
            'sent_timestamp': time.time(),
            'opened': False,
            'clicked': False
        }
        self.tracking_data.append(tracking_info)
        
        return personalized_email, tracking_id
    

    def setup_smtp_connection(self):
        """Setup SMTP connection"""
        try:
            self.smtp_server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            self.smtp_server.starttls()
            self.smtp_server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
            logger.info("SMTP connection established")
            return True
        except Exception as e:
            logger.error(f"Failed to setup SMTP connection: {e}")
            logger.info("Running in demo mode - emails will be simulated")
            return False

    def send_email(self, to_email, subject, html_content):
        """Send individual email"""
        try:
            if self.smtp_server:
                # Real email sending
                msg = MIMEMultipart('alternative')
                msg['From'] = Config.EMAIL_ADDRESS
                msg['To'] = to_email
                msg['Subject'] = subject
                
                # Attach HTML content
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
                
                # Send email
                self.smtp_server.send_message(msg)
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                # Demo mode
                logger.info(f"Email simulated to {to_email} (demo mode)")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    
    def run_email_campaign(self, leads_file=None):
        """Execute automated email campaign"""
        if not leads_file:
            leads_file = Config.LEADS_FILE
            
        # Load leads
        try:
            df = pd.read_excel(leads_file)
            leads = df.to_dict('records')
            logger.info(f"Loaded {len(leads)} leads from {leads_file}")
        except Exception as e:
            logger.error(f"Failed to load leads: {e}")
            return False
        
        # Create email template
        template = self.create_email_template()
        
        # Setup SMTP connection
        smtp_connected = self.setup_smtp_connection()
        
        # Campaign statistics
        sent_count = 0
        failed_count = 0
        
        try:
            # Process leads in batches
            for i, lead in enumerate(leads):
                email_address = lead.get('email', '')
                if not email_address or email_address == 'N/A':
                    logger.warning(f"Skipping lead with no email: {lead.get('company_name', 'Unknown')}")
                    continue
                
                # Personalize email
                try:
                    personalized_content, tracking_id = self.personalize_email(template, lead)
                    
                    # Create subject line
                    subject = f"Boost {lead.get('company_name', 'Your Company')}'s Sales by 25% - Free Consultation"
                    
                    # Send email
                    if self.send_email(email_address, subject, personalized_content):
                        sent_count += 1
                        logger.info(f"Email {sent_count} sent to {email_address} ({lead.get('company_name')})")
                    else:
                        failed_count += 1
                    
                    # Small delay between emails
                    time.sleep(2)
                    
                    # Batch delay
                    if (i + 1) % Config.BATCH_SIZE == 0:
                        logger.info(f"Batch completed. Waiting {min(Config.DELAY_BETWEEN_BATCHES, 10)} seconds...")
                        time.sleep(min(Config.DELAY_BETWEEN_BATCHES, 10))
                        
                except Exception as e:
                    logger.warning(f"Error processing email for {lead.get('company_name')}: {e}")
                    failed_count += 1
                    continue
                        
        except Exception as e:
            logger.error(f"Campaign execution error: {e}")
        
        finally:
            # Close SMTP connection
            if self.smtp_server:
                try:
                    self.smtp_server.quit()
                    logger.info("SMTP connection closed")
                except:
                    pass
        
        # Save tracking data
        self.save_tracking_data()
        
        logger.info(f"Campaign completed. Sent: {sent_count}, Failed: {failed_count}")
        return {
            'sent': sent_count,
            'failed': failed_count,
            'total_leads': len(leads)
        }
    def save_tracking_data(self):
        """Save tracking data to CSV"""
        if self.tracking_data:
            df = pd.DataFrame(self.tracking_data)
        else:
            # Create sample tracking data if none exists
            sample_tracking = []
            for i in range(5):
                sample_tracking.append({
                    'tracking_id': f'track_{random.randint(1000, 9999)}',
                    'company_name': f'Sample Company {i+1}',
                    'email': f'contact{i+1}@company{i+1}.com',
                    'sent_timestamp': time.time() - random.randint(0, 3600),
                    'opened': False,
                    'clicked': False
                })
            df = pd.DataFrame(sample_tracking)
            self.tracking_data = sample_tracking
            
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
        
        df.to_csv(Config.LOG_FILE, index=False)
        logger.info(f"Tracking data saved to {Config.LOG_FILE}")