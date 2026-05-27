def _fmt(amount):
    if amount < 0:
        return f"-{abs(amount):,.2f}"
    return f"{amount:,.2f}"


def format_payroll_message(employee, period):
    e = employee

    lines = [f"\U0001f4b0 급여 명세 ({period})", ""]

    if e["nick_name"]:
        lines.append(f"{e['name']} ({e['nick_name']}) 님")
    else:
        lines.append(f"{e['name']} 님")

    info_parts = []
    if e["unit"]:
        info_parts.append(f"숙소 {e['unit']}")
    if e["shift"]:
        info_parts.append(e["shift"])
    if e["total_hours"] > 0:
        info_parts.append(f"총 {e['total_hours']:g}시간")
    if info_parts:
        lines.append(" · ".join(info_parts))
    lines.append("")

    items = []
    if e["night_100"]:
        items.append(("야간수당", e["night_100"]))
    if e["tip"]:
        items.append(("팁", e["tip"]))
    if e["table_bonus"]:
        items.append(("테이블보너스", e["table_bonus"]))
    if e["flight_ticket"]:
        items.append(("항공권", e["flight_ticket"]))
    if e["deduction_visa"]:
        items.append(("비자비용 차감", -abs(e["deduction_visa"])))
    if e["deduction_table"]:
        items.append(("테이블 차감", -abs(e["deduction_table"])))
    if e["electric_deduction"]:
        items.append(("전기세 차감", -abs(e["electric_deduction"])))
    if e["remarks"]:
        items.append(("선불금 차감", -abs(e["remarks"])))

    for label, amount in items:
        lines.append(f"  {label}  {_fmt(amount)}")

    lines.append("─────────────────────")
    lines.append(f"  실수령액 (USDT)  ${e['usdt_total']:,.2f}")

    if e["allowance"]:
        lines.append(f"  수당 (₱)  ₱{e['allowance']:,.0f}")

    return "\n".join(lines)
