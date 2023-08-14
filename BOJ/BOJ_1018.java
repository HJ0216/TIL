import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {

	public static boolean[][] arr;
	public static int min = 64;

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st = new StringTokenizer(br.readLine(), " ");

		int ROW = Integer.parseInt(st.nextToken());
		int COL = Integer.parseInt(st.nextToken());

		arr = new boolean[ROW][COL];

		for (int i = 0; i < ROW; i++) {
			String s = br.readLine();
			
			for (int j = 0; j < COL; j++) {
				if (s.charAt(j) == 'W') {
					arr[i][j] = true;
				}
			}
		}

		for (int i = 0; i < ROW - 7; i++) {
			for (int j = 0; j < COL - 7; j++) {
				check(i, j);
			}
		}

		bw.write(min + "");

		bw.flush();
		bw.close();
	}

	public static void check(int x, int y) {
		int cnt = 0;
		
		boolean value = arr[x][y];

		for (int i = x; i < x + 8; i++) {
			for (int j = y; j < y + 8; j++) {
				if (arr[i][j] != value) {
					cnt++;
				}
				value = (!value);
			}
			value = (!value);
		}

		cnt = Math.min(cnt, 64 - cnt);

		min = Math.min(min, cnt);
	}
}
