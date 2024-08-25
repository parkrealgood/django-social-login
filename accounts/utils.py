from requests_oauthlib import OAuth1Session


def get_oauth1_session(
        client_key: str, client_secret: str, callback_uri: str = '',
        resource_owner_key: str = '', resource_owner_secret: str = '', verifier: str = ''
) -> OAuth1Session:
    """OAuth1Session 객체 반환"""
    return OAuth1Session(
        client_key=client_key,
        client_secret=client_secret,
        callback_uri=callback_uri,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier
    )
