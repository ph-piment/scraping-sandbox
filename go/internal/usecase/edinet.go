package usecase

import (
	"context"
	"fmt"

	"scraping-sandbox/internal/domain"
	"scraping-sandbox/internal/infra/notification"
)

type EdinetUsecase interface {
	NotifyBigHolders(ctx context.Context, date, channelID string) error
}
type edinetUsecase struct {
	edinetRepo domain.EdinetRepository
	slack      notification.Slack
}

func NewEdinetUsecase(
	edinetRepo domain.EdinetRepository,
	slack notification.Slack,
) EdinetUsecase {
	return &edinetUsecase{
		edinetRepo: edinetRepo,
		slack:      slack,
	}
}

func (u *edinetUsecase) NotifyBigHolders(ctx context.Context, date, channelID string) error {
	edinetCodeEntries, err := u.edinetRepo.LoadEdinetCodeEntries()
	if err != nil {
		return err
	}
	bigHolders, err := u.edinetRepo.FetchBigHolders(ctx, date)
	if err != nil {
		return err
	}
	return u.slack.Notify(channelID, u.buildBigHolderMessage(date, edinetCodeEntries, bigHolders))
}

func (u *edinetUsecase) buildBigHolderMessage(date string, edinetCodeEntries []domain.EdinetCodeEntry, bigHolders []domain.EdinetDoc) string {
	edinetCodeEntriesMap := make(map[string]domain.EdinetCodeEntry)
	for _, entry := range edinetCodeEntries {
		edinetCodeEntriesMap[entry.Code] = entry
	}

	msg := fmt.Sprintf("📢 Large shareholding reports have been submitted (%s)\n\n", date)
	for i, doc := range bigHolders {
		issuerName := edinetCodeEntriesMap[doc.IssuerEdinetCode].Name
		msg += fmt.Sprintf(
			"%d. %s (Filed by: %s)\n📅 Date submitted: %s\n📄 Document title: %s\n🔗 https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/%s.pdf\n\n",
			i+1,
			issuerName,
			doc.FilerName,
			doc.SubmitDateTime,
			doc.DocDescription,
			doc.DocID,
		)
	}
	return msg
}
