# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.exceptions import ValidationError
import logging
import json
import requests
from datetime import datetime

_logger = logging.getLogger(__name__)


class NotificationService(models.AbstractModel):
    _name = 'notification.service'
    _description = 'Dịch vụ Gửi Thông báo'

    @api.model
    def send_notification(self, log_record, send_immediately=False):
        """Gửi thông báo email/SMS"""
        try:
            results = {'email': None, 'sms': None}

            if log_record.notification_type in ['email', 'email_sms']:
                results['email'] = self._send_email(log_record)

            if log_record.notification_type in ['sms', 'email_sms']:
                results['sms'] = self._send_sms(log_record)

            # Cập nhật log
            email_id = results['email'].get('id') if results['email'] else None
            sms_id = results['sms'].get('id') if results['sms'] else None
            
            log_record.log_sent(
                email_external_id=email_id,
                sms_external_id=sms_id
            )

            _logger.info(f'✅ Gửi thông báo thành công: {log_record.subject}')
            return True

        except Exception as e:
            log_record.log_error(str(e))
            _logger.error(f'❌ Lỗi gửi thông báo: {str(e)}')
            return False

    def _send_email(self, log_record):
        """Gửi email"""
        from notify_email_config import NotifyEmailConfig

        try:
            config = NotifyEmailConfig.get_active_config()

            if config.email_provider == 'gmail':
                return self._send_gmail(config, log_record)
            elif config.email_provider == 'smtp':
                return self._send_smtp(config, log_record)
            elif config.email_provider == 'sendgrid':
                return self._send_sendgrid(config, log_record)

        except Exception as e:
            _logger.error(f'Email Error: {str(e)}')
            raise ValidationError(f'Lỗi gửi email: {str(e)}')

    def _send_gmail(self, config, log_record):
        """Gửi email qua Gmail API"""
        try:
            import base64
            from email.mime.text import MIMEText
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build
        except ImportError:
            raise ValidationError('Vui lòng cài đặt: google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client')

        try:
            # Parse service account JSON
            service_account_info = json.loads(config.gmail_service_account_json)
            
            # Create credentials
            credentials = Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/gmail.send']
            )

            # Build Gmail service
            service = build('gmail', 'v1', credentials=credentials)

            # Create message
            message = MIMEText(log_record.email_body_text or log_record.email_body)
            message['to'] = log_record.email_to
            message['from'] = config.gmail_sender_email
            message['subject'] = log_record.subject_line or log_record.subject

            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            # Send message
            result = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            return {'id': result['id']}

        except Exception as e:
            raise ValidationError(f'Gmail Error: {str(e)}')

    def _send_smtp(self, config, log_record):
        """Gửi email qua SMTP"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = log_record.subject_line or log_record.subject
            msg['From'] = f"{config.sender_name} <{config.smtp_username}>"
            msg['To'] = log_record.email_to
            
            if config.reply_to_email:
                msg['Reply-To'] = config.reply_to_email

            # Attach text part
            if log_record.email_body_text:
                msg.attach(MIMEText(log_record.email_body_text, 'plain'))
            
            # Attach HTML part if available
            if log_record.email_body:
                msg.attach(MIMEText(log_record.email_body, 'html'))

            # Connect and send
            if config.smtp_use_tls:
                server = smtplib.SMTP(config.smtp_host, config.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port)

            server.login(config.smtp_username, config.smtp_password)
            server.send_message(msg)
            server.quit()

            return {'id': msg['Message-ID']}

        except Exception as e:
            raise ValidationError(f'SMTP Error: {str(e)}')

    def _send_sendgrid(self, config, log_record):
        """Gửi email qua SendGrid"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Email, To, Content
        except ImportError:
            raise ValidationError('Vui lòng cài đặt: sendgrid')

        try:
            mail = Mail(
                from_email=Email(config.sendgrid_sender_email, config.sender_name),
                to_emails=To(log_record.email_to),
                subject=log_record.subject_line or log_record.subject,
                plain_text_content=log_record.email_body_text,
                html_content=log_record.email_body
            )

            if config.reply_to_email:
                mail.reply_to = Email(config.reply_to_email)

            sg = SendGridAPIClient(config.sendgrid_api_key)
            response = sg.send(mail)

            return {'id': response.headers.get('X-Message-Id', 'unknown')}

        except Exception as e:
            raise ValidationError(f'SendGrid Error: {str(e)}')

    def _send_sms(self, log_record):
        """Gửi SMS"""
        from notify_sms_config import NotifySmsConfig

        try:
            config = NotifySmsConfig.get_active_config()

            if config.sms_provider == 'viettel':
                return self._send_viettel_sms(config, log_record)
            elif config.sms_provider == 'twilio':
                return self._send_twilio_sms(config, log_record)
            elif config.sms_provider == 'aws_sns':
                return self._send_aws_sns_sms(config, log_record)

        except Exception as e:
            _logger.error(f'SMS Error: {str(e)}')
            raise ValidationError(f'Lỗi gửi SMS: {str(e)}')

    def _send_viettel_sms(self, config, log_record):
        """Gửi SMS qua Viettel"""
        try:
            payload = {
                'cpCode': config.viettel_cp_code,
                'username': config.viettel_username,
                'password': config.viettel_password,
                'senderID': config.viettel_sender,
                'receiver': log_record.sms_to,
                'message': log_record.sms_message[:160],  # Max 160 characters
            }

            response = requests.post(
                config.viettel_api_url,
                json=payload,
                timeout=10
            )

            if response.status_code not in [200, 201]:
                raise ValidationError(f'Viettel API Error: {response.text}')

            result = response.json()
            return {'id': result.get('messageId', 'unknown')}

        except Exception as e:
            raise ValidationError(f'Viettel SMS Error: {str(e)}')

    def _send_twilio_sms(self, config, log_record):
        """Gửi SMS qua Twilio"""
        try:
            from twilio.rest import Client
        except ImportError:
            raise ValidationError('Vui lòng cài đặt: twilio')

        try:
            client = Client(config.twilio_account_sid, config.twilio_auth_token)
            
            message = client.messages.create(
                body=log_record.sms_message,
                from_=config.twilio_phone_number,
                to=log_record.sms_to
            )

            return {'id': message.sid}

        except Exception as e:
            raise ValidationError(f'Twilio SMS Error: {str(e)}')

    def _send_aws_sns_sms(self, config, log_record):
        """Gửi SMS qua AWS SNS"""
        try:
            import boto3
        except ImportError:
            raise ValidationError('Vui lòng cài đặt: boto3')

        try:
            session = boto3.Session(
                aws_access_key_id=config.aws_access_key,
                aws_secret_access_key=config.aws_secret_key,
                region_name=config.aws_region
            )
            
            sns = session.client('sns')
            
            response = sns.publish(
                PhoneNumber=log_record.sms_to,
                Message=log_record.sms_message
            )

            return {'id': response['MessageId']}

        except Exception as e:
            raise ValidationError(f'AWS SNS Error: {str(e)}')
