FROM owasp/modsecurity-crs:nginx

USER root

# Create folder for custom rules + logs
RUN mkdir -p /etc/nginx/custom-waf /var/log/modsecurity /etc/nginx/modsecurity.d

# Correct permissions
RUN chown -R nginx:nginx /etc/modsecurity.d \
    /etc/nginx/modsecurity.d \
    /var/log/modsecurity \
    /etc/nginx/custom-waf

# Copy unicode mapping file to the location required by CRS
COPY unicode.mapping /etc/nginx/modsecurity.d/unicode.mapping
RUN chown nginx:nginx /etc/nginx/modsecurity.d/unicode.mapping

# Copy CRS overrides and custom rules
COPY rules/crs-setup.conf /etc/nginx/custom-waf/crs-setup.conf
COPY rules/custom-rules.conf /etc/nginx/custom-waf/custom-rules.conf

# Custom NGINX proxy config
COPY nginx.conf /etc/nginx/conf.d/custom.conf
RUN chown nginx:nginx /etc/nginx/conf.d/custom.conf

USER nginx

CMD ["nginx", "-g", "daemon off;"]
