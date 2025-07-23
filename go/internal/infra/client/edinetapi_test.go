package client_test

import (
	"bytes"
	"context"
	"io"
	"net/http"

	"scraping-sandbox/internal/infra/client"
	"scraping-sandbox/test/mocks/clientfakes"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("EdinetAPI", func() {
	var (
		ctx    context.Context
		apiKey string
	)

	BeforeEach(func() {
		ctx = context.Background()
		apiKey = "dummy-api-key"
	})

	Context("FetchDocumentJSON", func() {
		It("returns JSON on success", func() {
			// Set up mock Doer
			fakeClient := &clientfakes.FakeDoer{}
			respBody := `{"message": "ok"}`
			fakeClient.DoReturns(&http.Response{
				StatusCode: http.StatusOK,
				Body:       io.NopCloser(bytes.NewBufferString(respBody)),
			}, nil)

			api := &client.ExportEdinetAPI{
				Client:  fakeClient,
				BaseURL: "https://api.edinet-fsa.go.jp/api/v2/documents.json",
				ApiKey:  apiKey,
			}

			data, err := api.FetchDocumentJSON(ctx, "2025-08-06", "2")
			Expect(err).To(BeNil())
			Expect(string(data)).To(ContainSubstring("ok"))

			req := fakeClient.DoArgsForCall(0)
			Expect(req.URL.Query().Get("date")).To(Equal("2025-08-06"))
			Expect(req.URL.Query().Get("type")).To(Equal("2"))
			Expect(req.URL.Query().Get("Subscription-Key")).To(Equal(apiKey))
		})

		It("returns error when response code is not 200", func() {
			fakeClient := &clientfakes.FakeDoer{}
			fakeClient.DoReturns(&http.Response{
				StatusCode: http.StatusBadRequest,
				Body:       io.NopCloser(bytes.NewBufferString("bad request")),
			}, nil)

			api := &client.ExportEdinetAPI{
				Client:  fakeClient,
				BaseURL: "https://api.edinet-fsa.go.jp/api/v2/documents.json",
				ApiKey:  apiKey,
			}

			data, err := api.FetchDocumentJSON(ctx, "2025-08-06", "2")
			Expect(err).To(HaveOccurred())
			Expect(data).To(BeNil())
		})
	})
})
