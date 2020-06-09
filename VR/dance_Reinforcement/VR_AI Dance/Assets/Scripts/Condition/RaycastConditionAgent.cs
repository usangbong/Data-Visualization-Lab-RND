using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RaycastConditionAgent : Agent
{
    public GameObject objList;

    public int raySel;

    int select;

    CorWrong cw;

    void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();

        StartCoroutine(timeChecker());
    }

    public override void CollectObservations()
    {
        AddVectorObs(select);
        AddVectorObs(raySel);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        if(raySel == select)
        {
            AddReward(1f);
            cw.correct++;
        }

        else
        {
            AddReward(-0.2f);
            cw.wrong++;
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
