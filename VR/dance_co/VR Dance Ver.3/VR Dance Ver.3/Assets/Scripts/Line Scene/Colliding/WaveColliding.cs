using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WaveColliding : MonoBehaviour
{
    public Material yellow, green, red, black, blue;
    CircleMove circleMove;
    PlayAnim anim;
    GameObject obj;
    bool isColliding, isColor, isBlue;

    void Start()
    {
        circleMove = GameObject.Find("WaveManager").GetComponent<CircleMove>();
        anim = GameObject.Find("WaveIn1").GetComponent<PlayAnim>();
        isColliding = isColor = isBlue = false;
        obj = null;
    }

    void Update()
    {
        if(obj != null && circleMove.waveColorFinish && !anim.animFinish)
        {
            obj.transform.GetComponent<MeshRenderer>().material.color = Color.white;
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(circleMove.isWaveMakeFinish && !isColor)
            {
                if (gameObject.tag == "wave1") {
                    gameObject.transform.GetComponent<MeshRenderer>().material = black;
                    other.GetComponent<MeshRenderer>().material = black;
                }

                else if (gameObject.tag == "wave2")
                {
                    gameObject.transform.GetComponent<MeshRenderer>().material = yellow;
                    other.GetComponent<MeshRenderer>().material = yellow;
                }

                else if (gameObject.tag == "wave3")
                {
                    gameObject.transform.GetComponent<MeshRenderer>().material = red;
                    other.GetComponent<MeshRenderer>().material = red;
                }

                else if (gameObject.tag == "wave4")
                {
                    gameObject.transform.GetComponent<MeshRenderer>().material = green;
                    other.GetComponent<MeshRenderer>().material = green;
                }

                obj = other.gameObject;

                circleMove.colorNum++;
                isColor = true;
            }

            if (circleMove.waveColorFinish && !circleMove.rotFinish)
            {
                if(gameObject.tag == "wave1" && !circleMove.rot1)
                {
                    circleMove.rot1 = true;
                    circleMove.rotCnt++;
                }

                else if (gameObject.tag == "wave2" && !circleMove.rot2)
                {
                    circleMove.rot2 = true;
                    circleMove.rotCnt++;
                }

                else if (gameObject.tag == "wave3" && !circleMove.rot3)
                {
                    circleMove.rot3 = true;
                    circleMove.rotCnt++;
                }

                else if (gameObject.tag == "wave4" && !circleMove.rot4)
                {
                    circleMove.rot4 = true;
                    circleMove.rotCnt++;
                }
            }

            if(anim.animFinish && !isBlue)
            {
                gameObject.transform.GetComponent<MeshRenderer>().material = blue;

                circleMove.blueNum++;
                isBlue = true;

                obj = other.gameObject;
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isColliding = false;
        }
    }
}
