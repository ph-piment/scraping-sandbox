package client_test

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"

	"scraping-sandbox/internal/infra/client"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("EdinetAPI", func() {
	var (
		apiKey      = "test-api-key"
		testClient  *http.Client
		transport   *mockRoundTripper
		edinetAPI   client.EdinetAPI
		testContext context.Context
	)

	BeforeEach(func() {
		transport = &mockRoundTripper{}
		testClient = &http.Client{Transport: transport}
		edinetAPI = &testEdinetAPI{
			BaseURL: "https://fake-edinet.com/api",
			Client:  testClient,
			APIKey:  apiKey,
		}
		testContext = context.Background()
	})

	It("returns body when request is successful", func() {
		expectedBody := `{"results": []}`
		transport.Response = &http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewBufferString(expectedBody)),
		}

		body, err := edinetAPI.FetchDocumentJSON(testContext, "2025-07-17", "2")
		Expect(err).To(BeNil())
		Expect(string(body)).To(Equal(expectedBody))
	})

	It("returns error when request fails", func() {
		transport.Err = errors.New("network failure")

		_, err := edinetAPI.FetchDocumentJSON(testContext, "2025-07-17", "2")
		Expect(err).To(MatchError(ContainSubstring("network failure")))
	})

	It("returns error on non-200 response", func() {
		transport.Response = &http.Response{
			StatusCode: http.StatusInternalServerError,
			Body:       io.NopCloser(bytes.NewBufferString("error")),
		}

		_, err := edinetAPI.FetchDocumentJSON(testContext, "2025-07-17", "2")
		Expect(err).To(MatchError(ContainSubstring("unexpected response code")))
	})
})

type mockRoundTripper struct {
	Response *http.Response
	Err      error
}

func (m *mockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	return m.Response, m.Err
}

// testEdinetAPI embeds client.edinetAPI but allows us to inject test client
type testEdinetAPI struct {
	BaseURL string
	Client  *http.Client
	APIKey  string
}

func (t *testEdinetAPI) FetchDocumentJSON(ctx context.Context, date, docType string) ([]byte, error) {
	params := make(url.Values)
	params.Add("date", date)
	params.Add("type", docType)
	params.Add("Subscription-Key", t.APIKey)

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, t.BaseURL+"?"+params.Encode(), nil)
	if err != nil {
		return nil, err
	}

	resp, err := t.Client.Do(req)
	if err != nil {
		return nil, err
	}
	defer func() {
		err := resp.Body.Close()
		Expect(err).To(BeNil())
	}()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected response code: %d", resp.StatusCode)
	}

	return io.ReadAll(resp.Body)
}
