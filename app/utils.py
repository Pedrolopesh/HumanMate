from typing import Dict, List, Optional
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def read_yesno(prompt: str, default: bool = False) -> bool:
    suf = " [S/n]: " if default else " [s/N]: "
    while True:
        v = input(prompt + suf).strip().lower()
        if v == "" and default: return True
        if v == "" and not default: return False
        if v in ("s","sim","y","yes"): return True
        if v in ("n","nao","não","no"): return False
        print("Digite s para sim ou n para não.")

def read_decimal(prompt: str, positivo: bool = True, casas_quant: bool = False) -> Decimal:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("Valor obrigatório.")
            continue
        normalizado = raw.replace(".", "").replace(",", ".")
        try:
            v = Decimal(normalizado)
            if positivo and v <= 0:
                print("Valor deve ser maior que zero.")
                continue
            v = v.quantize(Decimal("0.000")) if casas_quant else v.quantize(Decimal("0.01"))
            return v
        except InvalidOperation:
            print("Valor inválido. Exemplos: 10, 99.90, 1.234,56")

def read_date(prompt: str, default_today: bool = True) -> date:
    while True:
        raw = input(prompt + (" (DD/MM/AAAA, Enter=hoje): " if default_today else " (DD/MM/AAAA): ")).strip()
        if raw == "" and default_today:
            return date.today()
        try:
            return datetime.strptime(raw, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use DD/MM/AAAA.")

def _print_opcoes(opcoes: List[str]):
    for i, nome in enumerate(opcoes, start=1):
        print(f"[{i}] {nome}")

def read_choice(opcoes: List[str], prompt: str) -> str:
    while True:
        _print_opcoes(opcoes)
        raw = input(prompt).strip()
        try:
            idx = int(raw)
            if 1 <= idx <= len(opcoes):
                return opcoes[idx - 1]
        except ValueError:
            pass
        print(f"Opção inválida. Digite um número entre 1 e {len(opcoes)}.")

def read_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s: return s
        print("Valor obrigatório.")

def formatar_tempo(segundos: int) -> str:
    if segundos is None:
        return "–"

    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60

    return f"{h}h {m}m {s}s"