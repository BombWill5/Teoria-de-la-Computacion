/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.automata_finito_determinista;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

/**
 *
 * @author JESG
 */
public class Automata_finito_determinista
{
    public static boolean q0(String cadena)
    {
        if (cadena.length() == 0)
            return true;
        else
        {
            if(cadena.charAt(0) == '0')
                return q1(cadena.substring(1));
            else
                return q2(cadena.substring(1));
        }
    }
    
    public static boolean q1(String cadena)
    {
        if (cadena.length() == 0)
            return false;
        else
        {
            if(cadena.charAt(0) == '0')
                return q0(cadena.substring(1));
            else
                return q3(cadena.substring(1));
        }
    }
    
    public static boolean q2(String cadena)
    {
        if (cadena.length() == 0)
            return false;
        else
        {
            if(cadena.charAt(0) == '0')
                return q3(cadena.substring(1));
            else
                return q0(cadena.substring(1));
        }
    }
    
    public static boolean q3(String cadena)
    {
        if (cadena.length() == 0)
            return false;
        else
        {
            if(cadena.charAt(0) == '0')
                return q2(cadena.substring(1));
            else
                return q1(cadena.substring(1));
        }
    }
   
    public static void main(String[] args) {
            int bandera;
            int contador = 1;
            Random rand = new Random();
            bandera = rand.nextInt(2);
            System.out.println(bandera);
            while(bandera == 1)
            {
                String rutaCadenas = "C:/Users/JESG/OneDrive - Instituto Politecnico Nacional/Documents/ArchivosAutomata/Cadenas" + contador + ".txt";
                String rutaPar = "C:/Users/JESG/OneDrive - Instituto Politecnico Nacional/Documents/ArchivosAutomata/Par" + contador + ".txt";
                String rutaImpar = "C:/Users/JESG/OneDrive - Instituto Politecnico Nacional/Documents/ArchivosAutomata/Impar" + contador + ".txt";
                String[] cadenas = new String[1000000];
                for (int i = 0; i < 1000000; i++)
                {
                    String cadena64 = "";
                    for (int j = 0; j < 64; j++)
                    {
                        
                        cadena64 += rand.nextInt(2);

                    }
                    cadenas[i] = cadena64;
                }
                
                System.out.println("Enviando...");
                try
                {
                    Thread.sleep(2000);
                }
                catch (InterruptedException e)
                {
                    e.printStackTrace();
                }
                
                try (PrintWriter writerCadenas = new PrintWriter(new FileWriter(rutaCadenas));
                 PrintWriter writerPar = new PrintWriter(new FileWriter(rutaPar));
                 PrintWriter writerImpar = new PrintWriter(new FileWriter(rutaImpar)))
                {
                    for (int i = 0; i < 1000000; i++)
                    {
                        writerCadenas.println(cadenas[i]);

                        if(q0(cadenas[i])) {
                            writerPar.println(cadenas[i]);
                        } else {
                            writerImpar.println(cadenas[i]);
                        }
                    }
                }
            catch (IOException e)
            {
                System.err.println("Error al escribir en el archivo: " + e.getMessage());
            }
                
                System.out.println("Finalizado");
                contador++;
                bandera = rand.nextInt(2);
                System.out.println(bandera);
            }
            System.out.println("Envios finalizados");
        }
}
