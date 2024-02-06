
const v_afternow = (value) => {
    let seldate = new Date(value)
    let today = new Date()
    return (
        seldate.valueOf() >= today.valueOf() - 86400000 || "No dates in the past"
    )
}
const v_length2 = (value) => {
    const l = value && value.length >= 2
    return l || "Too short"
}
const v_positive = (value) => value >= 0 || "Value must be positive"
const v_required = (value) => !!value || "Field required"
export { v_afternow, v_length2, v_positive, v_required }