export async function POST(req) {
  const data = await req.json();
  const { tipoCaminhao, tipoCarga, distanciaKm } = data;

  const consumoKmPorLitro = 3.5;
  const precoDiesel = 6.0;
  const precoArla = 5.0;
  const diariaMotorista = 120;
  const manutencaoPorKm = 0.25;
  const pedagioPorEixoKm = 0.20;
  const eixos = tipoCaminhao === "Cavalo 3 eixos" ? 6 : 2;

  const dieselTotal = (distanciaKm / consumoKmPorLitro) * precoDiesel;
  const arlaTotal = (dieselTotal / 20) * precoArla;
  const manutencao = distanciaKm * manutencaoPorKm;
  const pedagio = distanciaKm * pedagioPorEixoKm * eixos;
  const diaria = diariaMotorista * Math.ceil(distanciaKm / 500);
  const seguro = tipoCarga === "Perigosa" ? 150 : 50;

  const custoTotal = dieselTotal + arlaTotal + manutencao + pedagio + diaria + seguro;
  const freteFinal = custoTotal * 1.2;

  return Response.json({
    custoTotal: custoTotal.toFixed(2),
    freteFinal: freteFinal.toFixed(2),
    detalhes: {
      dieselTotal,
      arlaTotal,
      manutencao,
      pedagio,
      diaria,
      seguro
    }
  });
}