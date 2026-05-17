from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import padding


# Generate keys
private_key = rsa.generate_private_key(

    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()


# Generate signature
def generate_signature(message):

    signature = private_key.sign(

        message.encode(),

        padding.PSS(

            mgf=padding.MGF1(hashes.SHA256()),

            salt_length=padding.PSS.MAX_LENGTH
        ),

        hashes.SHA256()
    )

    return signature


# Verify signature
def verify_signature(message, signature):

    try:

        public_key.verify(

            signature,

            message.encode(),

            padding.PSS(

                mgf=padding.MGF1(hashes.SHA256()),

                salt_length=padding.PSS.MAX_LENGTH
            ),

            hashes.SHA256()
        )

        return True

    except:

        return False