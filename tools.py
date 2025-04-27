import requests
from agents import function_tool, RunContextWrapper
from context import UserContext
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:3000/api/f887dc57-d660-43d5-8fcf-afd6748cf9d9/billboards"

post_url = "http://localhost:3000/api/f887dc57-d660-43d5-8fcf-afd6748cf9d9/billboards/external"


@function_tool
def fetch_all_billboards() -> dict:
    try:
        logger.info(f"Fetching all billboards from {API_BASE}")
        response = requests.get(API_BASE, timeout=10)
        response.raise_for_status()
        return {"billboards": response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in fetch_all_billboards: {str(e)}")
        return {"error": f"Connection problem: {str(e)}"}


@function_tool
def fetch_billboard_by_id(billboard_id: str) -> dict:
    try:
        url = f"{API_BASE}/{billboard_id}/external"
        logger.info(f"Fetching billboard {billboard_id} from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {"billboard": response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in fetch_billboard_by_id: {str(e)}")
        return {"error": f"Connection problem: {str(e)}"}


@function_tool
def create_billboard(
    wrapper: RunContextWrapper[UserContext], label: str, imageUrl: str
) -> dict:
    try:
        userId = wrapper.context.userId
        logger.info(
            f"Creating billboard with userId: {userId}, label: {label}")
        headers = {"Content-Type": "application/json"}
        data = {"userId": userId, "label": label, "imageUrl": imageUrl}
        response = requests.post(
            post_url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return {"success": True, "billboard": response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in create_billboard: {str(e)}")
        return {"error": f"Connection problem: {str(e)}"}


@function_tool
def update_billboard(
    wrapper: RunContextWrapper[UserContext],
    billboard_id: str,
    label: str,
    imageUrl: str,
) -> dict:
    try:
        userId = wrapper.context.userId
        logger.info(f"Updating billboard {billboard_id} with userId: {userId}")
        url = f"{API_BASE}/{billboard_id}/external"
        headers = {"Content-Type": "application/json"}
        data = {"userId": userId, "label": label, "imageUrl": imageUrl}
        response = requests.patch(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return {"success": True, "billboard": response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in update_billboard: {str(e)}")
        return {"error": f"Connection problem: {str(e)}"}


@function_tool
def delete_billboard(
    wrapper: RunContextWrapper[UserContext], billboard_id: str
) -> dict:
    try:
        userId = wrapper.context.userId
        logger.info(f"Deleting billboard {billboard_id} with userId: {userId}")
        url = f"{API_BASE}/{billboard_id}/external"
        headers = {"Content-Type": "application/json"}
        data = {"userId": userId}
        response = requests.delete(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return {"success": True, "billboard": response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in delete_billboard: {str(e)}")
        return {"error": f"Connection problem: {str(e)}"}
