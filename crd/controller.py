import kopf
import requests
from kubernetes import client, config

# Load the in-cluster or local kubeconfig
try:
    config.load_incluster_config()
except:
    config.load_kube_config()


# -------------------------------------------------------------------
# Event handler: Trigger on creation of DummySite
# -------------------------------------------------------------------
@kopf.on.create('shujaakbar.com', 'v1alpha1', 'dummysites')
def create_dummysite(spec, name, namespace, logger, **kwargs):

    website_url = spec['website_url']
    logger.info(f"Fetching HTML from: {website_url}")

    # ---------------------------------------------------------------
    # Fetch HTML
    # ---------------------------------------------------------------
    try:
        response = requests.get(website_url)
        html_content = response.text
    except Exception as e:
        logger.error(f"Failed to download HTML: {e}")
        raise kopf.PermanentError("Failed to download HTML from website_url")

    # ---------------------------------------------------------------
    # Create ConfigMap with index.html
    # ---------------------------------------------------------------
    cm_name = f"{name}-html"
    v1 = client.CoreV1Api()

    cm_body = client.V1ConfigMap(
        metadata=client.V1ObjectMeta(
            name=cm_name,
            namespace=namespace,
            owner_references=[make_owner_reference(kind="DummySite")]
        ),
        data={"index.html": html_content}
    )

    v1.create_namespaced_config_map(namespace, cm_body)
    logger.info(f"Created ConfigMap {cm_name}")

    # ---------------------------------------------------------------
    # Return status fields
    # ---------------------------------------------------------------
    return {
        "htmlFetched": True,
        "message": f"Fetched HTML from {website_url}."
    }


# -------------------------------------------------------------------
# Helper: Generate OwnerReference to link resources with CR
# -------------------------------------------------------------------
def make_owner_reference(kind):
    return client.V1OwnerReference(
        api_version="shujaakbar.com/v1alpha1",
        kind=kind,
        controller=True,
        block_owner_deletion=True,
        name="{{name}}",        # Filled by Kopf automatically
        uid="{{uid}}"           # Filled by Kopf automatically
    )
