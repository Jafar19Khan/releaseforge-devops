FROM nginx:alpine
LABEL org.opencontainers.image.title="ReleaseForge DevOps Demo" \
      org.opencontainers.image.description="Static demo site for a Jenkins and Docker assignment"
COPY devopsIQ/ /usr/share/nginx/html/devopsIQ/
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/devopsIQ/ || exit 1
