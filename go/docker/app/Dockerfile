FROM golang:1.25.1-alpine3.22

WORKDIR /app

RUN apk update && \
    apk add --no-cache git curl tzdata

RUN go install mvdan.cc/gofumpt@v0.8.0

RUN go install golang.org/x/tools/cmd/goimports@v0.35.0

ENV PATH=$PATH:/go/bin

COPY . .

RUN go mod tidy
