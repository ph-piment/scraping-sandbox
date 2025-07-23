package client

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
)

type EdinetAPI interface {
	FetchDocumentJSON(ctx context.Context, date, docType string) ([]byte, error)
}

type edinetAPI struct {
	baseURL string
	client  *http.Client
	apiKey  string
}

func NewTransport(apiKey string) EdinetAPI {
	return &edinetAPI{
		baseURL: "https://api.edinet-fsa.go.jp/api/v2/documents.json",
		client:  http.DefaultClient,
		apiKey:  apiKey,
	}
}

func (t *edinetAPI) FetchDocumentJSON(ctx context.Context, date, docType string) ([]byte, error) {
	params := url.Values{}
	params.Add("date", date)
	params.Add("type", docType)
	params.Add("Subscription-Key", t.apiKey)

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, t.baseURL+"?"+params.Encode(), nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	resp, err := t.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer func() {
		if err := resp.Body.Close(); err != nil {
			log.Printf("failed to close response body: %v", err)
		}
	}()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected response code: %d", resp.StatusCode)
	}

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %w", err)
	}

	return bodyBytes, nil
}
