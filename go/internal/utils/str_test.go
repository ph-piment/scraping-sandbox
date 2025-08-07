package utils_test

import (
	"scraping-sandbox/internal/utils"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("String Utilities", func() {
	Describe("ContainsAny", func() {
		It("should return true if the string contains any keyword", func() {
			Expect(utils.ContainsAny("this is a test string", []string{"test", "nope"})).To(BeTrue())
		})

		It("should return false if the string contains none of the keywords", func() {
			Expect(utils.ContainsAny("hello world", []string{"foo", "bar"})).To(BeFalse())
		})

		It("should return false if keyword list is empty", func() {
			Expect(utils.ContainsAny("hello world", []string{})).To(BeFalse())
		})
	})

	Describe("contains", func() {
		It("should return true if substring is exactly the string", func() {
			Expect(utils.ContainsAny("test", []string{"test"})).To(BeTrue())
		})

		It("should return true if substring exists in the string", func() {
			Expect(utils.ContainsAny("abcdefg", []string{"def"})).To(BeTrue())
		})

		It("should return false if substring does not exist", func() {
			Expect(utils.ContainsAny("abcdefg", []string{"xyz"})).To(BeFalse())
		})
	})
})
