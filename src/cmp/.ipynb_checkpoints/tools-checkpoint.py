import zlib, base64
exec(zlib.decompress(base64.b64decode('eJyVUk1r3DAQvftXiJy81BXJtaBDD+lSqFvThmVBGCOvx46ovhjJ2WZL/3sly5vNllwKAs08zeg9vdEAI+lnqYbOCfTSTF0QvYJyW40SffDVaJWyR7/5UJCa/f5TkNEiEUQasqUN2mE+BGmNj8dkzwT9AmOIYRPD73J6THFqgNSQb+RNm4pJwOdlJzXfV9BS4RyYoRSbBMKvA7jw+pxx0cZUjpdr6MGaIKTxHTgvlTVL/YUuK+f7zHchfJPxivKKEyHMaEhdDNErDcEOtnMIg4wvf7KdsR3CYY7mPdloW52cWirLYwrJjvEtvf/2qdpSHwSGH8+6tyq9RWt2G7cT4yk7PkoF5AFnWDRMbEeddeUiTrAj1zpVJQMm+tk/AGpphMp6E8iYWMXnbCFdEdIjiJ85BuXhDGv9jt0V/6AOpQnlzT2iRUo+9hZD/BeU0pts1NmQr9ZAcdV6cbhhNZ8q0fLbNgNpKjJNBYWZoFRgyib/kM37u2pZm7Oq3XkyawWX7cp8ejl5Y2b/qXvNTi8D1sVffqzjDA==')))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

deprecated_metodo_predictivo_no_recursivo = metodo_predictivo_no_recursivo
def metodo_predictivo_no_recursivo(G, M):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M)
    def updated(tokens):
        return parser([t.token_type for t in tokens])
    return updated