class Args:
    register_weid = {
        "functionArg": {
        },
        "transactionArg": {
        },
        "functionName": "createWeId",
        "v": "1.0.0"
    }

    get_weid_doc = {
        "functionArg": {
            "weId": "did:weid:0x12025448644151248e5c1115b23a3fe55f4158e4153"
        },
        "transactionArg": {
        },
        "functionName": "getWeIdDocument",
        "v": "1.0.0"
    }

    register_authority_issuer = {
        "functionArg": {
            "weid": "did:weid:0x1Ae5b88d37327830307ab8da0ec5D8E8692A35D3",
            "name": "Sample College"
        },
        "transactionArg": {
            "invokerWeId": "ecdsa_key"
        },
        "functionName": "registerAuthorityIssuer",
        "v": "1.0.0"
    }

    select_authority_issuer = {
        "functionArg": {
            "weId": "did:weid:0x1ae5b88d37327830307ab8da0ec5d8e8692a35d3"
        },
        "transactionArg": {
        },
        "functionName": "queryAuthorityIssuer",
        "v": "1.0.0"
    }

    create_cpt = {
        "functionArg": {
            "weId": "did:weid:0x1ae5b88d37327830307ab8da0ec5d8e8692a35d3",
            "cptJsonSchema": {
                "title": "cpt",
                "description": "this is cpt",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "the name of certificate owner"
                    },
                    "gender": {
                        "enum": [
                            "F",
                            "M"
                        ],
                        "type": "string",
                        "description": "the gender of certificate owner"
                    },
                    "age": {
                        "type": "number",
                        "description": "the age of certificate owner"
                    }
                },
                "required": [
                    "name",
                    "age"
                ]
            }
        },
        "transactionArg": {
            "invokerWeId": "did:weid:0x1ae5b88d37327830307ab8da0ec5d8e8692a35d3"
        },
        "functionName": "registerCpt",
        "v": "1.0.0"
    }

    select_cpt = {
        "functionArg": {
            "cptId": 10,
        },
        "transactionArg": {
        },
        "functionName": "queryCpt",
        "v": "1.0.0"
    }

    create_credential = {
        "functionArg": {
            "cptId": 10,
            "issuer": "did:weid:0x12025448644151248e5c1115b23a3fe55f4158e4153",
            "expirationDate": "2100-04-18T21:12:33Z",
            "claim": {
                "name": "zhang san",
                "gender": "F",
                "age": 18
            },
        },
        "transactionArg": {
            "invokerWeId": "did:weid:0x12025448644151248e5c1115b23a3fe55f4158e4153"
        },
        "functionName": "createCredential",
        "v": "1.0.0"
    }

    verify_credential = {
        "functionArg": {
            "@context": "https://github.com/WeBankFinTech/WeIdentity/blob/master/context/v1",
            "claim": {
                "content": "b1016358-cf72-42be-9f4b-a18fca610fca",
                "receiver": "did:weid:101:0x7ed16eca3b0737227bc986dd0f2851f644cf4754",
                "weid": "did:weid:101:0xfd28ad212a2de77fee518b4914b8579a40c601fa"
            },
            "cptId": 2000156,
            "expirationDate": "2100-04-18T21:12:33Z",
            "id": "da6fbdbb-b5fa-4fbe-8b0c-8659da2d181b",
            "issuanceDate": "2020-02-06T22:24:00Z",
            "issuer": "did:weid:101:0xfd28ad212a2de77fee518b4914b8579a40c601fa",
            "proof": {
                "created": "1580999040000",
                "creator": "did:weid:101:0xfd28ad212a2de77fee518b4914b8579a40c601fa",
                "signature": "G0XzzLY+MqUAo3xXkS3lxVsgFLnTtvdXM24p+G5hSNNMSIa5vAXYXXKl+Y79CO2ho5DIGPPvSs2hvAixmfIJGbw=",
                "type": "Secp256k1"
            }
        },
        "transactionArg": {
        },
        "functionName": "verifyCredential",
        "v": "1.0.0"
    }
