# Actividad_Cliente_Servidor

```text
Actividad_Cliente_Servidor
│
├── pki/                     # Zona de certificados y scripts de la CA
│   ├── generate_ca.sh       # Script en Bash para crear la CA y certificados
│   ├── ca.crt               # Certificado de la Autoridad Certificadora
│   ├── server.crt           # Certificado del servidor (firmado por la CA)
│   └── server.key           # Llave privada del servidor
│
├── core_network/            # Requerimientos 1, 2 y 3
│   ├── unsecure_server.py   # Servidor sin cifrado (para comparar)
│   ├── unsecure_client.py   # Cliente sin cifrado
│   ├── tls_server.py        # Servidor seguro con TLS y validación de CA
│   └── tls_client.py        # Cliente seguro que valida la cadena de confianza
│
├── vpn_system/              # Requerimientos 6, 7 y 8 (AAA)
│   ├── remote_vpn.py        # Servidor de acceso remoto y autenticación de usuarios
│   └── site_to_site.py      # Simulación de túnel entre dos redes
│
├── ipsec_sim/               # Requerimiento 5 (Modos e IPsec / Anti-Replay)
│   └── ipsec_simulation.py  # Simulación de cabeceras, transporte/túnel y ventana anti-replay
│
└── logs/
    └── security.log         # Archivo centralizado de auditoría (AAA)
```
