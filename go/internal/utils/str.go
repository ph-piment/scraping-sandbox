package utils

func ContainsAny(s string, keywords []string) bool {
	for _, k := range keywords {
		if contains(s, k) {
			return true
		}
	}
	return false
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || (len(s) > len(substr) && (s[0:len(substr)] == substr || contains(s[1:], substr))))
}
