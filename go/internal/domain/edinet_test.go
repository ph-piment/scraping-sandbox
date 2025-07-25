package domain_test

import (
	. "scraping-sandbox/internal/domain"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("EdinetDoc", func() {
	Describe("IsLargeShareholdingReport", func() {
		Context("when the document is a large shareholding report", func() {
			It("should return true if doc type is 350 and description contains '大量保有'", func() {
				doc := EdinetDoc{
					DocTypeCode:    DocTypeCodeLargeShareholdingReport,
					DocDescription: "これは大量保有に関する報告です。",
				}
				Expect(doc.IsLargeShareholdingReport()).To(BeTrue())
			})

			It("should return true if doc type is 351 and description contains '変更報告'", func() {
				doc := EdinetDoc{
					DocTypeCode:    DocTypeCodeLargeShareholdingAmendment,
					DocDescription: "これは変更報告書です。",
				}
				Expect(doc.IsLargeShareholdingReport()).To(BeTrue())
			})

			It("should return false if doc type is 350 but description does not contain keywords", func() {
				doc := EdinetDoc{
					DocTypeCode:    DocTypeCodeLargeShareholdingReport,
					DocDescription: "This is a random report.",
				}
				Expect(doc.IsLargeShareholdingReport()).To(BeFalse())
			})
		})

		Context("when the document is not a large shareholding report", func() {
			It("should return false even if the description contains '大量保有'", func() {
				doc := EdinetDoc{
					DocTypeCode:    DocTypeCodeAnnualSecuritiesReport,
					DocDescription: "大量保有について言及があります。",
				}
				Expect(doc.IsLargeShareholdingReport()).To(BeFalse())
			})

			It("should return false if doc type is unknown and description is empty", func() {
				doc := EdinetDoc{
					DocTypeCode:    "999",
					DocDescription: "",
				}
				Expect(doc.IsLargeShareholdingReport()).To(BeFalse())
			})
		})
	})
})
