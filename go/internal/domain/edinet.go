package domain

import (
	"context"

	"scraping-sandbox/internal/utils"
)

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 -generate

//counterfeiter:generate -o ../../test/mocks/repositoryfakes . EdinetRepository
type EdinetRepository interface {
	FetchBigHolders(ctx context.Context, date string) ([]EdinetDoc, error)
	LoadEdinetCodeEntries() ([]EdinetCodeEntry, error)
}

const (
	// DocumentTypeMetadataOnly indicates only metadata should be retrieved (default).
	DocumentTypeMetadataOnly string = "1"

	// DocumentTypeWithDocuments indicates both the document list and metadata should be retrieved.
	DocumentTypeWithDocuments string = "2"
)

type EdinetResponse struct {
	Results []EdinetDoc `json:"results"`
}

type EdinetDoc struct {
	SeqNumber        int    `json:"seqNumber"`
	DocID            string `json:"docID"`
	EdinetCode       string `json:"edinetCode"`
	SecCode          string `json:"secCode"`
	JCN              string `json:"JCN"`
	FilerName        string `json:"filerName"`
	FundCode         string `json:"fundCode"`
	OrdinanceCode    string `json:"ordinanceCode"`
	FormCode         string `json:"formCode"`
	DocTypeCode      string `json:"docTypeCode"`
	PeriodStart      string `json:"periodStart"`
	PeriodEnd        string `json:"periodEnd"`
	SubmitDateTime   string `json:"submitDateTime"`
	DocDescription   string `json:"docDescription"`
	IssuerEdinetCode string `json:"issuerEdinetCode"`
	IssuerName       string `json:"issuerName"`
	FiledDate        string `json:"filedDate"`
	WithdrawalStatus string `json:"withdrawalStatus"`
}

const (
	DocTypeCodeSecuritiesRegistrationNew       string = "110" // 有価証券届出書（新規）
	DocTypeCodeSecuritiesRegistrationContinued string = "120" // 有価証券届出書（継続）
	DocTypeCodeSecuritiesRegistrationAmendment string = "130" // 有価証券届出書（訂正）
	DocTypeCodeSecuritiesRegistrationNotice    string = "140" // 有価証券届出書（訂正通知）
	DocTypeCodeAnnualSecuritiesReport          string = "210" // 有価証券報告書
	DocTypeCodeQuarterlyReport                 string = "220" // 四半期報告書
	DocTypeCodeSemiAnnualReport                string = "230" // 半期報告書
	DocTypeCodeExtraordinaryReport             string = "240" // 臨時報告書
	DocTypeCodeInternalControlReport           string = "250" // 内部統制報告書
	DocTypeCodeAmendedAnnualSecuritiesReport   string = "260" // 訂正有価証券報告書
	DocTypeCodeAmendedQuarterlyReport          string = "270" // 訂正四半期報告書
	DocTypeCodeAmendedSemiAnnualReport         string = "280" // 訂正半期報告書
	DocTypeCodeAmendedExtraordinaryReport      string = "290" // 訂正臨時報告書
	DocTypeCodeAmendedInternalControlReport    string = "300" // 訂正内部統制報告書
	DocTypeCodeLargeShareholdingReport         string = "350" // 大量保有報告書
	DocTypeCodeLargeShareholdingAmendment      string = "351" // 大量保有報告書（変更）
	DocTypeCodeLargeShareholdingCorrection     string = "352" // 大量保有報告書（訂正）
	DocTypeCodeTenderOfferNotification         string = "360" // 公開買付届出書
	DocTypeCodeOpinionReport                   string = "370" // 意見表明報告書
	DocTypeCodeTenderOfferProgressReport       string = "380" // 買付け等の状況報告書
	DocTypeCodeTenderOfferReport               string = "390" // 公開買付報告書
	DocTypeCodeOpinionReportTenderOffer        string = "400" // 意見表明報告書（公開買付）
	DocTypeCodeTenderOfferResultReport         string = "410" // 公開買付結果報告書
)

func (ed *EdinetDoc) IsLargeShareholdingReport() bool {
	switch ed.DocTypeCode {
	case DocTypeCodeLargeShareholdingReport,
		DocTypeCodeLargeShareholdingAmendment,
		DocTypeCodeLargeShareholdingCorrection:
		return containsBigHolderKeyword(ed.DocDescription)
	default:
		return false
	}
}

func containsBigHolderKeyword(desc string) bool {
	return utils.ContainsAny(desc, []string{"大量保有", "変更報告"})
}

type EdinetCodeEntry struct {
	Code            string `csv:"ＥＤＩＮＥＴコード"`
	SubmitterType   string `csv:"提出者種別"`
	ListedType      string `csv:"上場区分"`
	Consolidated    string `csv:"連結の有無"`
	Capital         string `csv:"資本金"`
	FiscalYearEnd   string `csv:"決算日"`
	Name            string `csv:"提出者名"`
	NameEnglish     string `csv:"提出者名（英字）"`
	NameKana        string `csv:"提出者名（ヨミ）"`
	Location        string `csv:"所在地"`
	Industry        string `csv:"提出者業種"`
	SecurityCode    string `csv:"証券コード"`
	CorporateNumber string `csv:"提出者法人番号"`
}
