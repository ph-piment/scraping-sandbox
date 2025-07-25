package usecase_test

import (
	"context"
	"errors"

	"scraping-sandbox/internal/domain"
	"scraping-sandbox/internal/usecase"
	"scraping-sandbox/test/mocks/notificationfakes"
	"scraping-sandbox/test/mocks/repositoryfakes"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("EdinetUsecase", func() {
	var (
		ctx         context.Context
		fakeRepo    *repositoryfakes.FakeEdinetRepository
		fakeSlack   *notificationfakes.FakeSlack
		usecaseImpl usecase.EdinetUsecase
	)

	BeforeEach(func() {
		ctx = context.Background()
		fakeRepo = new(repositoryfakes.FakeEdinetRepository)
		fakeSlack = new(notificationfakes.FakeSlack)

		usecaseImpl = usecase.NewEdinetUsecase(fakeRepo, fakeSlack)
	})

	Describe("NotifyBigHolders", func() {
		var (
			testDate  = "2025-07-17"
			channelID = "CHANNEL_XYZ"
			testDocs  = []domain.EdinetDoc{
				{
					DocID:            "DOC123",
					DocDescription:   "大量保有報告書",
					DocTypeCode:      domain.DocTypeCodeLargeShareholdingReport,
					IssuerEdinetCode: "E12345",
					FilerName:        "Filer Corp",
					SubmitDateTime:   "2025-07-17T10:00:00Z",
				},
			}
			testEntries = []domain.EdinetCodeEntry{
				{
					Code: "E12345",
					Name: "Test Corporation",
				},
			}
		)

		It("sends formatted big holder message to Slack", func() {
			fakeRepo.LoadEdinetCodeEntriesReturns(testEntries, nil)
			fakeRepo.FetchBigHoldersReturns(testDocs, nil)

			err := usecaseImpl.NotifyBigHolders(ctx, testDate, channelID)
			Expect(err).To(Succeed())

			Expect(fakeRepo.LoadEdinetCodeEntriesCallCount()).To(Equal(1))
			Expect(fakeRepo.FetchBigHoldersCallCount()).To(Equal(1))
			Expect(fakeSlack.NotifyCallCount()).To(Equal(1))

			notifiedChannel, message := fakeSlack.NotifyArgsForCall(0)
			Expect(notifiedChannel).To(Equal(channelID))
			Expect(message).To(ContainSubstring("📢 Large shareholding reports have been submitted (2025-07-17)"))
			Expect(message).To(ContainSubstring("Test Corporation"))
			Expect(message).To(ContainSubstring("https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/DOC123.pdf"))
		})

		It("returns error if LoadEdinetCodeEntries fails", func() {
			fakeRepo.LoadEdinetCodeEntriesReturns(nil, errors.New("csv error"))

			err := usecaseImpl.NotifyBigHolders(ctx, testDate, channelID)
			Expect(err).To(MatchError("csv error"))
			Expect(fakeSlack.NotifyCallCount()).To(Equal(0))
		})

		It("returns error if FetchBigHolders fails", func() {
			fakeRepo.LoadEdinetCodeEntriesReturns(testEntries, nil)
			fakeRepo.FetchBigHoldersReturns(nil, errors.New("api error"))

			err := usecaseImpl.NotifyBigHolders(ctx, testDate, channelID)
			Expect(err).To(MatchError("api error"))
			Expect(fakeSlack.NotifyCallCount()).To(Equal(0))
		})
	})
})
