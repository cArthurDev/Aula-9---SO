import java.util.ArrayList;
import java.util.Random;

public class SimuladorFIFO {

    private static final int RAM_SIZE = 10;
    private static final int SWAP_SIZE = 100;

    private static final int SIMULATION_STEPS = 1000;
    private static final int RESET_INTERVAL = 10;

    static class Pagina {
        int N, I, D, R, M, T;

        public Pagina(int n, int i, int d, int r, int m, int t) {
            this.N = n;
            this.I = i;
            this.D = d;
            this.R = r;
            this.M = m;
            this.T = t;
        }

        public Pagina(Pagina outra) {
            this.N = outra.N;
            this.I = outra.I;
            this.D = outra.D;
            this.R = outra.R;
            this.M = outra.M;
            this.T = outra.T;
        }
    }

    private static Pagina[] matrizSwap = new Pagina[SWAP_SIZE];

    private static ArrayList<Pagina> listaRam = new ArrayList<>(RAM_SIZE);

    private static Random rand = new Random();

    public static void main(String[] args) {

        inicializarSwap(matrizSwap);
        inicializarRam(listaRam, matrizSwap);

        System.out.println("--- ESTADO INICIAL (FIFO com ArrayList) ---");
        imprimirLista(listaRam, "LISTA RAM (Inicial)");
        imprimirArray(matrizSwap, "MATRIZ SWAP (Inicial)");
        System.out.println("--------------------------------------\n");

        executarSimulacaoFIFO();

        System.out.println("\n--- ESTADO FINAL (Após " + SIMULATION_STEPS + " instruções) ---");
        imprimirLista(listaRam, "LISTA RAM (Final)");
        imprimirArray(matrizSwap, "MATRIZ SWAP (Final)");
        System.out.println("--------------------------------------");
    }

    private static void inicializarSwap(Pagina[] swap) {
        for (int i = 0; i < SWAP_SIZE; i++) {
            int d = rand.nextInt(50) + 1;
            int t = rand.nextInt(9900) + 100;
            swap[i] = new Pagina(i, i + 1, d, 0, 0, t);
        }
    }

    private static void inicializarRam(ArrayList<Pagina> ram, Pagina[] swap) {
        for (int i = 0; i < RAM_SIZE; i++) {
            int linhaSwapSorteada = rand.nextInt(SWAP_SIZE);
            ram.add(new Pagina(swap[linhaSwapSorteada]));
        }
    }

    private static void executarSimulacaoFIFO() {
        int fifoPointer = 0;

        for (int i = 0; i < SIMULATION_STEPS; i++) {

            int instrucaoRequisitada = rand.nextInt(100) + 1;

            int indiceRam = buscarPaginaRam(instrucaoRequisitada);

            if (indiceRam != -1) {
                Pagina paginaHit = listaRam.get(indiceRam);
                paginaHit.R = 1;

                if (rand.nextDouble() < 0.50) {
                    paginaHit.D++;
                    paginaHit.M = 1;
                }

            } else {
                Pagina paginaSaindo = listaRam.get(fifoPointer);

                if (paginaSaindo.M == 1) {
                    int indiceSwap = paginaSaindo.N;
                    matrizSwap[indiceSwap] = new Pagina(paginaSaindo);
                    matrizSwap[indiceSwap].M = 0;
                }

                int indiceSwapEntrando = instrucaoRequisitada - 1;
                Pagina novaPagina = new Pagina(matrizSwap[indiceSwapEntrando]);

                listaRam.set(fifoPointer, novaPagina);

                fifoPointer = (fifoPointer + 1) % RAM_SIZE;
            }

            if ((i + 1) % RESET_INTERVAL == 0) {
                resetarBitR(listaRam);
            }
        }
    }

    private static int buscarPaginaRam(int instrucao) {
        for (int i = 0; i < listaRam.size(); i++) {
            if (listaRam.get(i).I == instrucao) {
                return i;
            }
        }
        return -1;
    }

    private static void resetarBitR(ArrayList<Pagina> ram) {
        for (Pagina p : ram) {
            p.R = 0;
        }
    }

    private static void imprimirLista(ArrayList<Pagina> lista, String nome) {
        System.out.println("\n== " + nome + " ==");
        System.out.printf("%-5s | %-5s | %-5s | %-3s | %-3s | %-5s\n", "N", "I", "D", "R", "M", "T");
        System.out.println("----------------------------------------");

        for (Pagina p : lista) {
            System.out.printf("%-5d | %-5d | %-5d | %-3d | %-3d | %-5d\n",
                    p.N, p.I, p.D, p.R, p.M, p.T);
        }
    }

    private static void imprimirArray(Pagina[] array, String nome) {
        System.out.println("\n== " + nome + " ==");
        System.out.printf("%-5s | %-5s | %-5s | %-3s | %-3s | %-5s\n", "N", "I", "D", "R", "M", "T");
        System.out.println("----------------------------------------");

        for (Pagina p : array) {
            System.out.printf("%-5d | %-5d | %-5d | %-3d | %-3d | %-5d\n",
                    p.N, p.I, p.D, p.R, p.M, p.T);
        }
    }
}