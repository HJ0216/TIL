import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Arrays;
import java.util.StringTokenizer;
 
public class Main {
    public static void main(String[] args) throws Exception {
 
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
 
        StringTokenizer st = new StringTokenizer(br.readLine(), " ");
        int row = Integer.parseInt(st.nextToken());
        int col = Integer.parseInt(st.nextToken());
        
        int[][] intArr1 = new int[row][col];
        for(int i=0; i<row; i++) {
            StringTokenizer stInner = new StringTokenizer(br.readLine(), " ");
            for(int j=0; j<col; j++) {
                intArr1[i][j] += Integer.parseInt(stInner.nextToken());
            }
        }
 
        int[][] intArr2 = new int[row][col];
        for(int i=0; i<row; i++) {
            StringTokenizer stInner = new StringTokenizer(br.readLine(), " ");
            for(int j=0; j<col; j++) {
                intArr1[i][j] += Integer.parseInt(stInner.nextToken());
            }
        }
        
        int[][] sumArr = new int[row][col];
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                sumArr[i][j] = intArr1[i][j] + intArr2[i][j];
            }
        }
 
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                bw.write(sumArr[i][j] + " ");
            }
            bw.newLine();
        }
        
        
        bw.flush();
        bw.close();
    }
}
