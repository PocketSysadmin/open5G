$TTL    604800
@       IN      SOA     ns1.dominio.com. admin.dominio.com. (
                        2023071601         ; Serial
                        604800         ; Refresh
                        86400         ; Retry
                        2419200         ; Expire
                        604800 )       ; Negative Cache TTL
;

@       IN      NS      ns1.dominio.com.
ns1     IN      A       172.21.5.5
