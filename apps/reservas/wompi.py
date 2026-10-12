import hashlib
import hmac


def generar_firma_integridad(
    referencia,
    valor_en_centavos,
    moneda,
    secreto,
):
    cadena = (
        f"{referencia}{valor_en_centavos}"
        f"{moneda}{secreto}"
    )
    return hashlib.sha256(
        cadena.encode("utf-8")
    ).hexdigest()


def verificar_firma_evento(evento, secreto):
    firma = evento.get("signature")
    datos = evento.get("data")
    if not isinstance(firma, dict):
        return False
    if not isinstance(datos, dict):
        return False

    propiedades = firma.get("properties")
    marca_tiempo = firma.get("timestamp")
    checksum = firma.get("checksum")
    if not isinstance(propiedades, list):
        return False
    if not propiedades:
        return False
    if isinstance(marca_tiempo, bool):
        return False
    if not isinstance(marca_tiempo, (str, int)):
        return False
    if not isinstance(checksum, str):
        return False

    valores = []
    for propiedad in propiedades:
        if not isinstance(propiedad, str):
            return False
        valor = datos
        for parte in propiedad.split("."):
            if not isinstance(valor, dict):
                return False
            if parte not in valor:
                return False
            valor = valor[parte]
        if valor is None:
            return False
        valores.append(str(valor))

    cadena = (
        "".join(valores)
        + str(marca_tiempo)
        + secreto
    )
    checksum_esperado = hashlib.sha256(
        cadena.encode("utf-8")
    ).hexdigest()
    return hmac.compare_digest(
        checksum_esperado.lower(),
        checksum.lower(),
    )
