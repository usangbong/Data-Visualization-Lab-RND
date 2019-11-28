using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayAnim : MonoBehaviour
{
    public Animation anim;
    public bool animFinish;
    float time;
    bool isTime, func;
    CircleMove circleMove;

    void Start()
    {
        circleMove = GameObject.Find("WaveManager").GetComponent<CircleMove>();
        time = 0.0f;
        isTime = func = false;
        animFinish = false;
    }

    void Update()
    {
        if(circleMove.makeWaveFinish)
        {
            if(!func)
            {
                StartCoroutine(timeChecker());
                func = true;
            }
            anim.Play("WaveToLinear");
        }

        if(isTime)
        {
            anim.Stop("WaveToLinear");
            animFinish = true;
        }
    }

    IEnumerator timeChecker()
    {
        while (!isTime)
        {
            time += 0.1f;
            if(time >= 1.3f)
            {
                isTime = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }
}
