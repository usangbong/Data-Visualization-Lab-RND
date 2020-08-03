using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;
using System.IO;

public class HeightCollocateTest : Agent
{
    public Transform pivot, target;

    IntegratedCorWrong cw;
    CollocateManager cm;

    int select;

    private void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<IntegratedCorWrong>();
        cm = GameObject.Find("setObjectManager").GetComponent<CollocateManager>();

        StartCoroutine(timeChecker());
    }

    public override void CollectObservations()
    {
        AddVectorObs(target.position.y);
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        if(select == 0)
        {
            if(target.position.y >= 1.65f)
            {
                cw.hCorrect++;
                cm.setTall(true);
                AddReward(1f);
            }

            else
            {
                cw.hWrong++;
                cm.setTall(false);
                AddReward(-1f);
            }
        }

        else if(select == 1)
        {
            if(target.position.y >= 1.65f)
            {
                cw.hWrong++;
                cm.setTall(true);
                AddReward(-1f);
            }

            else
            {
                cw.hCorrect++;
                cm.setTall(false);
                AddReward(1f);
            }
        }
    }

    IEnumerator timeChecker()
    {
        while (true)
        {
            yield return new WaitForSeconds(100f);

            cw.change = true;
            Done();
        }
    }
}
