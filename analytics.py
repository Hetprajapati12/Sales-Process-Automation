import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
import time
import os
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignAnalytics:
    def __init__(self):
        self.analytics_data = []
        
    def simulate_email_engagement(self, tracking_file=None):
        """Simulate email engagement data for demonstration"""
        if not tracking_file:
            tracking_file = Config.LOG_FILE
            
        try:
            # Check if file exists and has content
            if os.path.exists(tracking_file) and os.path.getsize(tracking_file) > 0:
                df = pd.read_csv(tracking_file)
                if df.empty:
                    df = self._create_sample_tracking_data()
            else:
                df = self._create_sample_tracking_data()
        except Exception as e:
            logger.warning(f"Error reading tracking file: {e}. Creating sample data.")
            df = self._create_sample_tracking_data()
        
        # Simulate engagement
        engagement_data = []
        for _, row in df.iterrows():
            # Simulate open rates (30-40%)
            opened = random.random() < 0.35
            # Simulate click rates (5-10% of total, higher for opened emails)
            clicked = opened and random.random() < 0.25
            
            # Categorize lead quality
            if clicked:
                lead_category = 'Hot'
            elif opened:
                lead_category = 'Warm'
            else:
                lead_category = 'Cold'
            
            engagement_data.append({
                'tracking_id': row.get('tracking_id', f'track_{random.randint(1000, 9999)}'),
                'company_name': row.get('company_name', f'Company {random.randint(1, 100)}'),
                'email': row.get('email', f'contact{random.randint(1, 100)}@company.com'),
                'sent_timestamp': row.get('sent_timestamp', time.time() - random.randint(0, 86400)),
                'opened': opened,
                'clicked': clicked,
                'lead_category': lead_category,
                'engagement_score': self._calculate_engagement_score(opened, clicked)
            })
        
        self.analytics_data = engagement_data
        return engagement_data
    
    def _create_sample_tracking_data(self):
        """Create sample tracking data when real data is not available"""
        sample_data = {
            'tracking_id': [f'track_{i}' for i in range(1, 11)],
            'company_name': [
                'TechInnovate Solutions', 'CloudFirst Analytics', 'Digital Growth Partners',
                'E-Commerce Accelerator', 'Strategic Business Advisors', 'InnovateTech Labs',
                'ScaleUp SaaS', 'Performance Marketing Group', 'NextGen Software Inc',
                'Professional Services Corp'
            ],
            'email': [
                'sarah.chen@techinnovatesolutions.com', 'michael@cloudfirstanalytics.com',
                'jennifer@digitalgrowthpartners.com', 'david.kim@ecommerceaccelerator.com',
                'lisa@strategicbusinessadvisors.com', 'alex@innovatetechlabs.com',
                'rachel@scaleupsaas.com', 'carlos@performancemarketinggroup.com',
                'info@nextgensoftware.com', 'contact@professionalservices.com'
            ],
            'sent_timestamp': [time.time() - random.randint(0, 86400) for _ in range(10)]
        }
        return pd.DataFrame(sample_data)
    
    def _calculate_engagement_score(self, opened, clicked):
        """Calculate engagement score based on actions"""
        score = 0
        if opened:
            score += 30
        if clicked:
            score += 70
        return score
    
    def generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        if not self.analytics_data:
            self.simulate_email_engagement()
        
        df = pd.DataFrame(self.analytics_data)
        
        # Calculate key metrics
        total_emails = len(df)
        opened_emails = df['opened'].sum()
        clicked_emails = df['clicked'].sum()
        
        open_rate = (opened_emails / total_emails) * 100 if total_emails > 0 else 0
        click_rate = (clicked_emails / total_emails) * 100 if total_emails > 0 else 0
        ctr = (clicked_emails / opened_emails) * 100 if opened_emails > 0 else 0
        
        # Lead categorization
        hot_leads = df[df['lead_category'] == 'Hot']
        warm_leads = df[df['lead_category'] == 'Warm']
        cold_leads = df[df['lead_category'] == 'Cold']
        
        report = {
            'campaign_metrics': {
                'total_emails_sent': total_emails,
                'emails_opened': opened_emails,
                'emails_clicked': clicked_emails,
                'open_rate': round(open_rate, 2),
                'click_rate': round(click_rate, 2),
                'click_through_rate': round(ctr, 2)
            },
            'lead_categorization': {
                'hot_leads': len(hot_leads),
                'warm_leads': len(warm_leads),
                'cold_leads': len(cold_leads),
                'hot_lead_percentage': round((len(hot_leads) / total_emails) * 100, 2),
                'conversion_potential': 'High' if len(hot_leads) > total_emails * 0.1 else 'Medium'
            },
            'top_performing_companies': hot_leads['company_name'].tolist(),
            'recommendations': self._generate_recommendations(open_rate, click_rate, len(hot_leads))
        }
        
        logger.info("Analytics report generated successfully")
        return report
    
    def _generate_recommendations(self, open_rate, click_rate, hot_leads_count):
        """Generate actionable recommendations based on metrics"""
        recommendations = []
        
        if open_rate < 20:
            recommendations.append("Low open rate detected. Consider improving subject lines and send timing.")
        elif open_rate > 40:
            recommendations.append("Excellent open rate! Your subject lines are performing well.")
        
        if click_rate < 5:
            recommendations.append("Low click rate. Consider improving email content and call-to-action.")
        elif click_rate > 10:
            recommendations.append("Great click rate! Your email content is engaging.")
        
        if hot_leads_count > 0:
            recommendations.append(f"You have {hot_leads_count} hot leads. Prioritize immediate follow-up.")
        
        return recommendations
    
    def create_visualizations(self):
        """Create interactive visualizations for campaign performance"""
        if not self.analytics_data:
            self.simulate_email_engagement()
        
        df = pd.DataFrame(self.analytics_data)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Campaign Overview', 'Lead Categories', 
                          'Engagement Timeline', 'Top Companies by Engagement'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # 1. Campaign Overview (Bar chart)
        metrics = ['Sent', 'Opened', 'Clicked']
        values = [len(df), df['opened'].sum(), df['clicked'].sum()]
        colors = ['#3498db', '#2ecc71', '#e74c3c']
        
        fig.add_trace(
            go.Bar(x=metrics, y=values, marker_color=colors, name='Campaign Metrics'),
            row=1, col=1
        )
        
        # 2. Lead Categories (Pie chart)
        category_counts = df['lead_category'].value_counts()
        fig.add_trace(
            go.Pie(labels=category_counts.index, values=category_counts.values, name='Lead Categories'),
            row=1, col=2
        )
        
        # 3. Engagement Timeline (Scatter plot)
        df['sent_date'] = pd.to_datetime(df['sent_timestamp'], unit='s')
        fig.add_trace(
            go.Scatter(
                x=df['sent_date'], 
                y=df['engagement_score'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=df['engagement_score'],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=df['company_name'],
                name='Engagement Over Time'
            ),
            row=2, col=1
        )
        
        # 4. Top Companies by Engagement
        top_companies = df.nlargest(5, 'engagement_score')
        fig.add_trace(
            go.Bar(
                x=top_companies['company_name'], 
                y=top_companies['engagement_score'],
                marker_color='#9b59b6',
                name='Top Companies'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title='Sales Campaign Analytics Dashboard',
            height=800,
            showlegend=False
        )
        
        # Save visualization
        fig.write_html('campaign_analytics.html')
        logger.info("Visualizations saved to campaign_analytics.html")
        
        return fig
    
    def export_detailed_report(self, filename='detailed_analytics_report.xlsx'):
        """Export detailed analytics to Excel"""
        if not self.analytics_data:
            self.simulate_email_engagement()
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Main analytics data
                df = pd.DataFrame(self.analytics_data)
                df.to_excel(writer, sheet_name='Email_Tracking', index=False)
                
                # Summary metrics
                report = self.generate_analytics_report()
                summary_df = pd.DataFrame([report['campaign_metrics']])
                summary_df.to_excel(writer, sheet_name='Campaign_Summary', index=False)
                
                # Lead categorization
                lead_cat_df = pd.DataFrame([report['lead_categorization']])
                lead_cat_df.to_excel(writer, sheet_name='Lead_Categories', index=False)
                
                # Hot leads details
                hot_leads_df = df[df['lead_category'] == 'Hot']
                hot_leads_df.to_excel(writer, sheet_name='Hot_Leads', index=False)
            
            logger.info(f"Detailed report exported to {filename}")
            
        except PermissionError:
            # Try alternative filename
            import time
            alt_filename = f"analytics_report_{int(time.time())}.xlsx"
            try:
                with pd.ExcelWriter(alt_filename, engine='openpyxl') as writer:
                    df = pd.DataFrame(self.analytics_data)
                    df.to_excel(writer, sheet_name='Email_Tracking', index=False)
                logger.info(f"Detailed report exported to {alt_filename}")
            except:
                # Final fallback to CSV
                df.to_csv('analytics_report.csv', index=False)
                logger.info("Detailed report exported to analytics_report.csv")
        
        return filename