from ..fastapidata import send_api
from ..models import ReportInfo, ScheduledMessage, CustomUser
from django.utils import timezone
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def schedule_subtract_coins(user, final_count):
    try:
        data = CustomUser.objects.get(email=user)
        if user is None or data.coins is None:
            logger.error("User or user coins not found.")
            return
        final_coins = final_count
        if data.coins >= final_coins:
            data.coins -= final_coins
            logger.info(f"Message sent successfully. Deducted {final_coins} coins from your account. Remaining balance: {data.coins}")
            data.save()
        else:
            logger.error("Insufficient coins to proceed.")
    except CustomUser.DoesNotExist:
        logger.error(f"User with email {user} does not exist.")
    except Exception as e:
        logger.error(f"Error while subtracting coins for user {user}: {str(e)}")

def subtract_coins(request, final_count):
    user = request.user
    if user is None or user.coins is None:
        messages.error(request, "User or user coins not found.")
        logger.error("User or user coins not found.")
        return
    final_coins = final_count
    if user.coins >= final_coins:
        user.coins -= final_coins
        logger.info(f"Coins deducted: {final_coins}. Remaining balance: {user.coins}")
        user.save()
        messages.success(request, f"Message sent successfully. Deducted {final_coins} coins from your account.")
    else:
        logger.error("Insufficient coins to proceed.")
        messages.error(request, "You don't have enough coins to proceed.")

def display_phonenumber_id(request):
    phonenumber_id = request.user.phone_number_id
    return phonenumber_id

def send_messages(current_user, token, phone_id, campaign_list, template_name, media_id, all_contact, contact_list, campaign_title, request):
    try:
        logger.info(f"Sending messages for user: {current_user}, campaign title: {campaign_title}")
        for campaign in campaign_list:
            if campaign['template_name'] == template_name:
                language = campaign['template_language']
                media_type = campaign['media_type']

                money_data = len(all_contact) + 0 * len(all_contact)
                logger.info(f"Calculated money data for sending messages: {money_data}")

                if request:
                    subtract_coins(request, money_data)
                else:
                    schedule_subtract_coins(current_user, money_data)
                logging.info(f"Sent message details: {token, phone_id, template_name, language, media_type, media_id, contact_list}")
                logging.info(f"Sent message details: {type(token), type(phone_id), type(template_name), type(language), type(media_type), type(media_id), type(contact_list)}")
                send_api(token, phone_id, template_name, language, media_type, media_id, contact_list)

        formatted_numbers = []
        for number in all_contact:
            if number.startswith("+91"):
                formatted_numbers.append("91" + number[3:])
            elif not number.startswith("91"):
                formatted_numbers.append("91" + number)
            else:
                formatted_numbers.append(number)

        phone_numbers_string = ",".join(formatted_numbers)

        ReportInfo.objects.create(
            email=str(current_user),
            campaign_title=campaign_title,
            contact_list=phone_numbers_string,
            message_date=timezone.now(),
            message_delivery=len(all_contact),
            template_name=template_name
        )
        logger.info(f"Messages sent successfully for campaign: {campaign_title}, user: {current_user}")
    except Exception as e:
        logger.error(f"Error in sending messages: {str(e)}")

def save_schedule_messages(current_user, template_name, media_id, all_contact, contact_list, campaign_title, schedule_date, schedule_time):
    try:
        data = ScheduledMessage(
            current_user=current_user,
            template_name=template_name,
            media_id=media_id,
            all_contact=all_contact,
            contact_list=contact_list,
            campaign_title=campaign_title,
            schedule_date=schedule_date,
            schedule_time=schedule_time
        )
        data.save()
        logger.info(f"Scheduled message saved for campaign: {campaign_title}, user: {current_user}")
    except Exception as e:
        logger.error(f"Error in saving scheduled messages: {str(e)}")
