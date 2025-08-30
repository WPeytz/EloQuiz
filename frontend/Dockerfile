FROM --platform=linux/amd64 node:lts-alpine

# static server
RUN npm install -g serve

WORKDIR /app

# install deps first for better caching
COPY package*.json ./
RUN npm ci

# copy the rest
COPY . .

# pass backend URL at build time (Vue CLI reads VUE_APP_* during build)
ARG VUE_APP_API_BASE
ENV VUE_APP_API_BASE=${VUE_APP_API_BASE}

# build production bundle
RUN npm run build

# Cloud Run sets PORT (e.g., 8080)
ENV PORT=8080
EXPOSE 8080

# bind to 0.0.0.0 and $PORT
CMD ["sh","-c","set -eux; echo PORT=${PORT:-8080}; which serve || true; node -v; npm -v; ls -lah dist || true; test -f dist/index.html; serve -s dist -l tcp://0.0.0.0:${PORT}"]

# # --- Build stage (Node) ---
# FROM node:20-alpine AS build
# WORKDIR /app

# # Install deps first (better layer caching)
# COPY package*.json ./
# RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# # Copy source and build
# COPY . .
# RUN npm run build

# # --- Runtime stage (Nginx) ---
# FROM nginx:alpine
# RUN apk add --no-cache gettext

# # Cloud Run sets PORT at runtime; default to 8080 locally
# ENV PORT=8080

# # Remove default site so only our template is active
# RUN rm -f /etc/nginx/conf.d/default.conf

# # Copy built assets from the build stage
# COPY --from=build /app/dist /usr/share/nginx/html

# # Nginx template that listens on $PORT and serves a Vue SPA
# RUN mkdir -p /etc/nginx/templates
# RUN printf "server {\n\
#     listen       $PORT;\n\
#     server_name  _;\n\
#     root   /usr/share/nginx/html;\n\
#     index  index.html;\n\
#     access_log /dev/stdout;\n\
#     error_log  /dev/stderr notice;\n\
# \n    # Serve JS: first try root (as referenced), then /js/ (where Vue usually emits)\n\
#     location ~* \\.js$ {\n\
#       try_files $$uri /js$$uri =404;\n\
#       add_header Cache-Control \"public, max-age=31536000, immutable\";\n\
#       access_log off;\n\
#     }\n\
# \n    # Serve CSS: first try root, then /css/\n\
#     location ~* \\.css$ {\n\
#       try_files $$uri /css$$uri =404;\n\
#       add_header Cache-Control \"public, max-age=31536000, immutable\";\n\
#       access_log off;\n\
#     }\n\
# \n    # Images / fonts and misc assets (do not rewrite these to index.html)\n\
#     location ~* \\.(?:ico|png|jpg|jpeg|gif|svg|webp|woff2?|ttf|map)$ {\n\
#       try_files $$uri =404;\n\
#       add_header Cache-Control \"public, max-age=31536000, immutable\";\n\
#       access_log off;\n\
#     }\n\
# \n    # Exact match so internal redirect to /index.html does not re-enter location /\n\
#     location = /index.html { }\n\
# \n    # SPA fallback for application routes\n\
#     location / {\n\
#       try_files $$uri $$uri/ /index.html;\n\
#     }\n\
# \n    # simple health endpoint\n\
#     location = /healthz { return 200 'ok'; add_header Content-Type text/plain; }\n\
# \n    # basic 50x page (internal)\n\
#     error_page 500 502 503 504 /50x.html;\n\
#     location = /50x.html { internal; return 500; }\n\
#   }\n" > /etc/nginx/templates/default.conf.template

# # Start Nginx with envsubst to inject $PORT at runtime and verify build output exists
# CMD ["/bin/sh","-c","set -eux; envsubst '$$PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf; echo '--- rendered nginx conf ---'; cat /etc/nginx/conf.d/default.conf; echo '--- listing /usr/share/nginx/html ---'; ls -lah /usr/share/nginx/html || true; test -f /usr/share/nginx/html/index.html; nginx -g 'daemon off;'"]