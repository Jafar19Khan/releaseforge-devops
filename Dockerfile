FROM nginx:stable-alpine
LABEL org.opencontainers.image.title="ReleaseForge" \
      org.opencontainers.image.description="Container delivery with automated validation and deployment verification"
RUN rm -f /etc/nginx/conf.d/default.conf
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY app/ /usr/share/nginx/html/
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/healthz || exit 1
