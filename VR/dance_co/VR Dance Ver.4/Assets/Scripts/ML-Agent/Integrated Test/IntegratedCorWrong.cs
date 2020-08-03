using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class IntegratedCorWrong : MonoBehaviour
{
    int time = 0;
    public int hCorrect = 0, hWrong = 0;
    public int vCorrect = 0, vWrong = 0;
    public int rCorrect = 0, rWrong = 0;
    public bool change = false;

    void Update()
    {
        if (change)
        {
            float hPer = getPercentage(hCorrect, hWrong);
            float vper = getPercentage(vCorrect, vWrong);
            float rPer = getPercentage(rCorrect, rWrong);

            time += 100;

            Debug.Log("time: " + time + "\n" + "Height: " + string.Format("{0:F2}", hPer) + "%, " +
                "Velocity: " + string.Format("{0:F2}", vper) + "%, " +
                "Radius: " + string.Format("{0:F2}", rPer) + "%");

            hCorrect = hWrong = vCorrect = vWrong = rCorrect = rWrong = 0;
            change = false;
        }
    }

    float getPercentage(int correct, int wrong)
    {
        float percentage = (System.Convert.ToSingle(correct) / System.Convert.ToSingle(correct + wrong)) * 100f;

        return percentage;
    }
}
