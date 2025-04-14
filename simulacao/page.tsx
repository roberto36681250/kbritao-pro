"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Page() {
  const [origem, setOrigem] = useState("");
  const [destino, setDestino] = useState("");
  const [tipoCarga, setTipoCarga] = useState("Comum");
  const [tipoCaminhao, setTipoCaminhao] = useState("Toco");
  const [distanciaKm, setDistanciaKm] = useState("");
  const router = useRouter();

  const simular = async () => {
    const res = await fetch("/api/calcular-frete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ origem, destino, tipoCarga, tipoCaminhao, distanciaKm: parseFloat(distanciaKm) })
    });
    const data = await res.json();
    localStorage.setItem("resultado", JSON.stringify(data));
    router.push("/resultados");
  };

  return (
    <main className="p-6 space-y-4">
      <h2 className="text-xl font-bold">🚚 Simulação de Frete</h2>
      <input type="text" placeholder="Origem" value={origem} onChange={e => setOrigem(e.target.value)} className="border p-2 w-full"/>
      <input type="text" placeholder="Destino" value={destino} onChange={e => setDestino(e.target.value)} className="border p-2 w-full"/>
      <select value={tipoCaminhao} onChange={e => setTipoCaminhao(e.target.value)} className="border p-2 w-full">
        <option>Toco</option>
        <option>Truck</option>
        <option>Cavalo 2 eixos</option>
        <option>Cavalo 3 eixos</option>
      </select>
      <select value={tipoCarga} onChange={e => setTipoCarga(e.target.value)} className="border p-2 w-full">
        <option>Comum</option>
        <option>Perigosa</option>
        <option>Refrigerada</option>
      </select>
      <input type="number" placeholder="Distância em km" value={distanciaKm} onChange={e => setDistanciaKm(e.target.value)} className="border p-2 w-full"/>
      <button onClick={simular} className="bg-green-700 text-white p-2 rounded w-full">Calcular Frete</button>
    </main>
  )
}