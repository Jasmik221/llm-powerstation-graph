from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class Bus(BaseModel):
    id: str = Field(min_length=1)
    vn_kv: float = Field(gt=0)


class Line(BaseModel):
    id: str = Field(min_length=1)
    from_bus: str = Field(min_length=1)
    to_bus: str = Field(min_length=1)
    length_km: float | None = Field(default=None, gt=0)


class Load(BaseModel):
    id: str = Field(min_length=1)
    bus: str = Field(min_length=1)
    p_mw: float = Field(gt=0)


class NetworkGraph(BaseModel):
    buses: list[Bus]
    lines: list[Line]
    loads: list[Load]

    @model_validator(mode="after")
    def check_references(self) -> NetworkGraph:
        all_ids = [item.id for group in (self.buses, self.lines, self.loads) for item in group]
        if len(all_ids) != len(set(all_ids)):
            raise ValueError("Identyfikatory elementów muszą być unikalne.")

        bus_ids = {bus.id for bus in self.buses}
        for line in self.lines:
            if line.from_bus not in bus_ids or line.to_bus not in bus_ids:
                raise ValueError(f"Linia {line.id} wskazuje niezdefiniowaną szynę.")
            if line.from_bus == line.to_bus:
                raise ValueError(f"Linia {line.id} musi łączyć dwie różne szyny.")
        for load in self.loads:
            if load.bus not in bus_ids:
                raise ValueError(f"Odbiór {load.id} wskazuje niezdefiniowaną szynę.")
        return self

    def as_property_graph(self) -> dict:
        nodes = [
            {"id": bus.id, "type": "Bus", "properties": {"vn_kv": bus.vn_kv}}
            for bus in self.buses
        ]
        nodes.extend(
            {
                "id": line.id,
                "type": "Line",
                "properties": {"length_km": line.length_km} if line.length_km is not None else {},
            }
            for line in self.lines
        )
        nodes.extend(
            {"id": load.id, "type": "Load", "properties": {"p_mw": load.p_mw}}
            for load in self.loads
        )

        relationships = []
        for line in self.lines:
            relationships.extend(
                [
                    {"type": "FROM_BUS", "from": line.id, "to": line.from_bus},
                    {"type": "TO_BUS", "from": line.id, "to": line.to_bus},
                ]
            )
        relationships.extend(
            {"type": "CONNECTED_TO", "from": load.id, "to": load.bus}
            for load in self.loads
        )
        return {"nodes": nodes, "relationships": relationships}
