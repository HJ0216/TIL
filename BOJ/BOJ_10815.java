import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int num1 = Integer.parseInt(br.readLine());

		int[] iArr1 = new int[num1];
		StringTokenizer st1 = new StringTokenizer(br.readLine());
		for (int i = 0; i < num1; i++) {
			iArr1[i] = Integer.parseInt(st1.nextToken());
		}

		Arrays.sort(iArr1);

		int num2 = Integer.parseInt(br.readLine());

		StringTokenizer st2 = new StringTokenizer(br.readLine());
		for (int i = 0; i < num2; i++) {
			bw.write(bSearch(iArr1, Integer.parseInt(st2.nextToken())) + " ");
		}

		bw.flush();
		bw.close();
	}

	public static int bSearch(int[] iArr1, int search) {
		int first = 0;
		int last = iArr1.length - 1;

		while (first <= last) {
			int mid = (first + last) / 2;

			if (iArr1[mid] == search) {
				return 1;
			}

			if (iArr1[mid] < search) {
				first = mid + 1;
			} else {
				last = mid - 1;
			}
		}

		return 0;

	}

}
