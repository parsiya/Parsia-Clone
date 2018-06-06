// Int64 returns the tag's i'th value as an integer. It returns an error if the
// tag's Format is not IntVal. It panics if i is out of range.
func (t *Tag) Int64(i int) (int64, error) {
	if t.format != IntVal {
		return 0, t.typeErr(IntVal)
	}
	return t.intVals[i], nil // <--- Panic
}