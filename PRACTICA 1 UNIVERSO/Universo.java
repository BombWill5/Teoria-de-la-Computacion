/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.universo;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import javax.swing.JFrame;

public class Universo {
    
    public static String Binario(int decimal, int corrida) {
        char[] binario = new char[corrida + 1];
        Arrays.fill(binario, '0');
        
        if (decimal == 0) {
            return new String(binario);
        }
        
        int residuo;
        int contador = 0;
        while (decimal > 0) {
            residuo = decimal % 2;
            if (residuo == 1) {
                binario[(binario.length - 1) - contador] = '1';
            }
            decimal = decimal / 2;
            contador++;
        }
        return new String(binario);
    }
    
    public static int contarCeros(String binario) {
        int cuenta = 0;
        for (char c : binario.toCharArray()) {
            if (c == '0') {
                cuenta++;
            }
        }
        return cuenta;
    }
    
    public static void generarGrafica(List<Integer> ceros, List<Integer> unos) {
        XYSeries serieCeros = new XYSeries("Ceros");
        XYSeries serieUnos = new XYSeries("Unos");

        XYSeries serieCerosLog = new XYSeries("Log10(Ceros)");
        XYSeries serieUnosLog = new XYSeries("Log10(Unos)");

        for (int i = 0; i < ceros.size(); i++) {
            int cantidadCeros = ceros.get(i);
            int cantidadUnos = unos.get(i);

            serieCeros.add(i + 1, cantidadCeros);  
            serieUnos.add(i + 1, cantidadUnos);

            double logCeros = Math.log10(cantidadCeros + 1);
            double logUnos = Math.log10(cantidadUnos + 1);

            serieCerosLog.add(i + 1, logCeros);
            serieUnosLog.add(i + 1, logUnos);
        }

        XYSeriesCollection datasetCeros = new XYSeriesCollection();
        datasetCeros.addSeries(serieCeros);

        XYSeriesCollection datasetUnos = new XYSeriesCollection();
        datasetUnos.addSeries(serieUnos);

        XYSeriesCollection datasetCerosLog = new XYSeriesCollection();
        datasetCerosLog.addSeries(serieCerosLog);

        XYSeriesCollection datasetUnosLog = new XYSeriesCollection();
        datasetUnosLog.addSeries(serieUnosLog);

        JFreeChart chartCeros = ChartFactory.createScatterPlot(
                "Número de Ceros por Cadena", "Cadena", "Cantidad de Ceros",
                datasetCeros, PlotOrientation.VERTICAL, true, true, false);

        JFreeChart chartUnos = ChartFactory.createScatterPlot(
                "Número de Unos por Cadena", "Cadena", "Cantidad de Unos",
                datasetUnos, PlotOrientation.VERTICAL, true, true, false);

        JFreeChart chartCerosLog = ChartFactory.createScatterPlot(
                "Log10(Número de Ceros) por Cadena", "Cadena", "Log10(Cantidad de Ceros)",
                datasetCerosLog, PlotOrientation.VERTICAL, true, true, false);

        JFreeChart chartUnosLog = ChartFactory.createScatterPlot(
                "Log10(Número de Unos) por Cadena", "Cadena", "Log10(Cantidad de Unos)",
                datasetUnosLog, PlotOrientation.VERTICAL, true, true, false);

        JFrame frameCeros = new JFrame("Gráfica de Ceros");
        frameCeros.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frameCeros.getContentPane().add(new ChartPanel(chartCeros));
        frameCeros.pack();
        frameCeros.setVisible(true);

        JFrame frameUnos = new JFrame("Gráfica de Unos");
        frameUnos.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frameUnos.getContentPane().add(new ChartPanel(chartUnos));
        frameUnos.pack();
        frameUnos.setVisible(true);

        JFrame frameCerosLog = new JFrame("Gráfica de Log10(Ceros)");
        frameCerosLog.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frameCerosLog.getContentPane().add(new ChartPanel(chartCerosLog));
        frameCerosLog.pack();
        frameCerosLog.setVisible(true);

        JFrame frameUnosLog = new JFrame("Gráfica de Log10(Unos)");
        frameUnosLog.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frameUnosLog.getContentPane().add(new ChartPanel(chartUnosLog));
        frameUnosLog.pack();
        frameUnosLog.setVisible(true);
    }


    public static void main(String[] args) {
        int opc;
        int n;
        Scanner scanner = new Scanner(System.in);

        while (true) {
            do {
                System.out.println("1) Elegir N\n2) Dejar que la maquina decida \n3) Salir");
                opc = scanner.nextInt();
            } while (opc != 1 && opc != 2 && opc != 3);

            if (opc == 3) {
                System.exit(0);
            }

            if (opc == 1) {
                do {
                    System.out.println("\nIngresa la N:");
                    n = scanner.nextInt();
                    System.out.println("\nN = " + n + "\n");
                } while (n < 0 || n > 1000);
            } else {
                Random rand = new Random();
                n = rand.nextInt(1000) + 1;
                System.out.println("\nN = " + n + "\n");
            }

            List<Integer> cerosList = new ArrayList<>();
            List<Integer> unosList = new ArrayList<>();

            try (PrintWriter writer = new PrintWriter(new FileWriter("C:/Users/JESG/OneDrive - Instituto Politecnico Nacional/Documents/salida.txt"))) {
                writer.print("Sigma* = {epsilon ");
                for (int i = 0; i < n - 1; i++) {
                    for (int j = 0; j < Math.pow(2, (i + 1)); j++) {
                        String binario = Binario(j, i);
                        writer.print(binario + ", ");

                        int ceros = contarCeros(binario);
                        int unos = binario.length() - ceros;

                        cerosList.add(ceros);
                        unosList.add(unos);
                    }
                    System.out.println("N = " + (i + 1));
                }

                for (int i = 0; i < Math.pow(2, n); i++) {
                    String binario = Binario(i, n - 1);
                    if (i == Math.pow(2, n) - 1)
                        writer.print(binario + "}");
                    else
                        writer.print(binario + ", ");

                    int ceros = contarCeros(binario);
                    int unos = binario.length() - ceros;

                    cerosList.add(ceros);
                    unosList.add(unos);
                }
                System.out.println("N = " + n);

                generarGrafica(cerosList, unosList);

            } catch (IOException e) {
                System.err.println("Error al escribir en el archivo: " + e.getMessage());
            }
        }
    }
}
