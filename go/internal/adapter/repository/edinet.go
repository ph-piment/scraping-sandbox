package repository

import (
	"bufio"
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"

	"scraping-sandbox/internal/domain"
	"scraping-sandbox/internal/infra/client"

	"golang.org/x/text/encoding/japanese"
	"golang.org/x/text/transform"
)

type edinetRepository struct {
	Transport client.EdinetAPI
}

func NewEdinetRepository(apiKey string) domain.EdinetRepository {
	return &edinetRepository{
		Transport: client.NewTransport(apiKey),
	}
}

func (repo *edinetRepository) FetchBigHolders(ctx context.Context, date string) ([]domain.EdinetDoc, error) {
	respBody, err := repo.Transport.FetchDocumentJSON(ctx, date, domain.DocumentTypeWithDocuments)
	if err != nil {
		return nil, err
	}

	var edinetResp domain.EdinetResponse
	err = json.Unmarshal(respBody, &edinetResp)
	if err != nil {
		return nil, fmt.Errorf("failed to decode response body: %w", err)
	}

	var docs []domain.EdinetDoc
	for _, doc := range edinetResp.Results {
		if doc.IsLargeShareholdingReport() {
			docs = append(docs, doc)
		}
	}
	return docs, nil
}

func (repo *edinetRepository) LoadEdinetCodeEntries() ([]domain.EdinetCodeEntry, error) {
	filePath := filepath.Join("internal", "data", "EdinetcodeDlInfo.csv")
	f, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open CSV file: %w", err)
	}
	defer func() {
		if err := f.Close(); err != nil {
			log.Printf("failed to close file: %v", err)
		}
	}()

	reader := transform.NewReader(bufio.NewReader(f), japanese.ShiftJIS.NewDecoder())

	csvReader := csv.NewReader(reader)
	csvReader.FieldsPerRecord = -1 // allow variable number of fields

	_, err = csvReader.Read()
	if err != nil {
		return nil, fmt.Errorf("failed to read CSV header: %w", err)
	}

	var entries []domain.EdinetCodeEntry

	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, fmt.Errorf("error while reading CSV: %w", err)
		}

		if len(record) < 13 {
			continue // skip incomplete records
		}

		entries = append(entries, domain.EdinetCodeEntry{
			Code:            record[0],
			SubmitterType:   record[1],
			ListedType:      record[2],
			Consolidated:    record[3],
			Capital:         record[4],
			FiscalYearEnd:   record[5],
			Name:            record[6],
			NameEnglish:     record[7],
			NameKana:        record[8],
			Location:        record[9],
			Industry:        record[10],
			SecurityCode:    record[11],
			CorporateNumber: record[12],
		})
	}

	return entries, nil
}
