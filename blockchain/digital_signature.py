from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import padding


# Generate public/private keys
private_key = rsa.generate_private_key(

    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()


# Sample land data
message = b"LAND101 | Sai | Odisha | Area: 12"


# Generate digital signature
signature = private_key.sign(

    message,

    padding.PSS(

        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),

    hashes.SHA256()
)

print("\nDigital Signature Generated Successfully!")


# Verify signature
try:

    public_key.verify(

        signature,
        message,

        padding.PSS(

            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),

        hashes.SHA256()
    )

    print("Signature VERIFIED")
    print("Data Integrity Maintained")

except:

    print("Signature Verification FAILED")