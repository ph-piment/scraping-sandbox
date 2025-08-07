package repository_test

import (
	"context"
	"fmt"
	"os"
	"path/filepath"

	"scraping-sandbox/internal/adapter/repository"
	"scraping-sandbox/internal/domain"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

// Mock transport layer
type mockTransport struct {
	ResponseBody []byte
	Err          error
}

func (m *mockTransport) FetchDocumentJSON(ctx context.Context, date, docType string) ([]byte, error) {
	return m.ResponseBody, m.Err
}

var _ = Describe("EdinetRepository", func() {
	var repo domain.EdinetRepository

	Describe("FetchBigHolders", func() {
		It("returns only large shareholding documents", func() {
			mockJSON := []byte(`{
				"results": [
					{
						"docID": "XYZ123",
						"docTypeCode": "350",
						"docDescription": "大量保有報告書",
						"issuerEdinetCode": "E12345",
						"filerName": "Test Filer",
						"submitDateTime": "2025-07-16T10:00:00Z"
					},
					{
						"docID": "XYZ456",
						"docTypeCode": "210",
						"docDescription": "有価証券報告書"
					}
				]
			}`)

			repo = &repository.ExportEdinetRepository{
				Transport: &mockTransport{ResponseBody: mockJSON},
			}

			docs, err := repo.FetchBigHolders(context.Background(), "2025-07-16")
			Expect(err).To(BeNil())
			Expect(docs).To(HaveLen(1))
			Expect(docs[0].DocID).To(Equal("XYZ123"))
		})
	})

	Describe("LoadEdinetCodeEntries", func() {
		var tmpDir string

		BeforeEach(func() {
			tmpDir = filepath.Join("internal", "data")
			err := os.MkdirAll(tmpDir, os.ModePerm)
			Expect(err).To(BeNil())

			content := []byte("ＥＤＩＮＥＴコード,提出者種別,上場区分,連結の有無,資本金,決算日,提出者名,提出者名（英字）,提出者名（ヨミ）,所在地,提出者業種,証券コード,提出者法人番号\n" +
				"AAA001,Type1,Listed,Yes,1000000,03/31,Company A,A Co.,カンパニーA,Tokyo,IT,1234,1234567890123\n")

			err = os.WriteFile(filepath.Join(tmpDir, "EdinetcodeDlInfo.csv"), content, 0o644)
			Expect(err).To(BeNil())
		})

		AfterEach(func() {
			err := os.RemoveAll(tmpDir)
			Expect(err).To(BeNil())
		})

		It("successfully loads Edinet code entries from CSV", func() {
			repo = repository.NewEdinetRepository("dummy-key")

			entries, err := repo.LoadEdinetCodeEntries()
			Expect(err).To(BeNil())
			Expect(entries).To(HaveLen(1))
			Expect(entries[0].Code).To(Equal("AAA001"))
			Expect(entries[0].Name).To(Equal("Company A"))
		})
	})

	Describe("FetchBigHolders error cases", func() {
		It("returns error when transport fails", func() {
			repo = &repository.ExportEdinetRepository{
				Transport: &mockTransport{
					Err: fmt.Errorf("network error"),
				},
			}

			_, err := repo.FetchBigHolders(context.Background(), "2025-07-16")
			Expect(err).To(HaveOccurred())
			Expect(err.Error()).To(ContainSubstring("network error"))
		})

		It("returns error when JSON is invalid", func() {
			repo = &repository.ExportEdinetRepository{
				Transport: &mockTransport{
					ResponseBody: []byte("invalid json"),
				},
			}

			_, err := repo.FetchBigHolders(context.Background(), "2025-07-16")
			Expect(err).To(HaveOccurred())
			Expect(err.Error()).To(ContainSubstring("failed to decode"))
		})
	})

	Describe("LoadEdinetCodeEntries error cases", func() {
		It("returns error when CSV file is missing", func() {
			_ = os.Remove(filepath.Join("internal", "data", "EdinetcodeDlInfo.csv"))
			repo = repository.NewEdinetRepository("dummy-key")

			_, err := repo.LoadEdinetCodeEntries()
			Expect(err).To(HaveOccurred())
			Expect(err.Error()).To(ContainSubstring("failed to open"))
		})

		It("skips incomplete rows gracefully", func() {
			tmpDir := filepath.Join("internal", "data")
			content := []byte("ヘッダー\n" +
				"A,B,C\n")
			_ = os.WriteFile(filepath.Join(tmpDir, "EdinetcodeDlInfo.csv"), content, 0o644)

			repo = repository.NewEdinetRepository("dummy-key")
			entries, err := repo.LoadEdinetCodeEntries()
			Expect(err).To(HaveOccurred())
			Expect(entries).To(HaveLen(0))
		})
	})
})
