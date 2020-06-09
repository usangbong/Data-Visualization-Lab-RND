using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CorWrong : MonoBehaviour
{
    public int correct = 0, wrong = 0, time = 0;
    public bool change = false;

    void Update()
    {
        if (change) 
        {
            float per = (System.Convert.ToSingle(correct) / System.Convert.ToSingle(correct + wrong)) * 100f;
            time += 100;
            Debug.Log("time: " + time + "\n" + "Correct: " + string.Format("{0:F2}", per) + "%");
            change = false;
            correct = wrong = 0;
        }
    }
}
